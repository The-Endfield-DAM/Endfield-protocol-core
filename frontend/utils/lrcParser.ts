// frontend/utils/lrcParser.ts

export interface LyricLine {
    time: number      // 秒数
    text: string      // 歌词内容 (可能包含换行符，即双语)
}

export function parseLrc(lrc: string): LyricLine[] {
    if (!lrc) return []

    const lines = lrc.split('\n')
    const rawEntries: LyricLine[] = []

    // 1. 宽松正则匹配: 支持 [mm:ss.xxx] [m:s.ms] 等多种格式
    // Group 1: min, Group 2: sec, Group 3: ms (optional)
    const timeReg = /\[(\d{1,3}):(\d{1,2})(?:\.(\d{1,3}))?\]/g

    for (const line of lines) {
        // 提取所有时间戳
        const matches = [...line.matchAll(timeReg)]
        if (matches.length === 0) continue

        // 提取歌词文本 (移除所有时间戳)
        const text = line.replace(timeReg, '').trim()
        if (!text) continue

        for (const match of matches) {
            const min = parseInt(match[1] || '0', 10)
            const sec = parseInt(match[2] || '0', 10)
            const msStr = match[3] || ''

            // 标准化毫秒: .5 -> 500ms, .05 -> 50ms, .005 -> 5ms
            const ms = msStr ? parseInt(msStr.padEnd(3, '0'), 10) : 0
            const time = min * 60 + sec + ms / 1000

            rawEntries.push({ time, text })
        }
    }

    // 2. 按时间排序
    rawEntries.sort((a, b) => a.time - b.time)

    // 3. 合并双语歌词 (时间差 < 0.2s)
    const result: LyricLine[] = []
    const hasChinese = (s: string) => /[\u4e00-\u9fa5]/.test(s)

    for (const entry of rawEntries) {
        const lastLine = result[result.length - 1]
        // 合并条件：时间接近 且 文本不同 (避免重复)
        if (lastLine && Math.abs(lastLine.time - entry.time) < 0.2) {
            if (lastLine.text !== entry.text) {
                // 智能排序：如果上一行是中文，当前行是外文(不含中文)，则把外文放到前面作为 Main
                // 这样可以修复 "中文译文在前，外文原文在后" 导致的显示错误
                if (hasChinese(lastLine.text) && !hasChinese(entry.text)) {
                    lastLine.text = `${entry.text}\n${lastLine.text}`
                } else {
                    lastLine.text += `\n${entry.text}`
                }
            }
        } else {
            result.push(entry)
        }
    }

    return result
}