// Renders the "Recommendations" section of README.md from tools.json.
//   node scripts/readme.ts          rewrite README.md
//   node scripts/readme.ts --check  fail if README.md is out of date
import { readFileSync, writeFileSync } from 'node:fs'
import { readTools, type Tool } from './registry.ts'

export const START = '<!-- tools:start -->'
export const END = '<!-- tools:end -->'

// README headings, in order. A category used in tools.json must be listed here.
export const CATEGORY_ORDER = [
  'GitHub Actions',
  'GitLab CI',
  'JavaScript and TypeScript',
  'Python',
  'Go',
  'Rust',
  'Ruby',
  'PHP',
  'Java',
  'Kotlin',
  '.NET',
  'Swift',
  'Elixir',
  'Shell',
  'Databases',
  'API contracts',
  'Web quality',
  'Tests and coverage',
  'Custom rules',
  'Secrets',
  'Vulnerabilities',
  'Dependency updates',
  'Docker, Terraform and Kubernetes',
  'Ansible',
  'Config files',
  'Policy',
  'Agent configuration',
  'Toolchain',
  'Git hooks',
  'Git conventions',
  'Documentation',
]

const entry = (tool: Tool): string => {
  const details = tool.details ? ` [Details](${tool.details}).` : ''
  return `- **[${tool.name}](https://github.com/${tool.repo})**: ${tool.rationale}${details}`
}

export function render(tools: Tool[]): string {
  const unknown = [...new Set(tools.map((tool) => tool.category))].filter((category) => !CATEGORY_ORDER.includes(category))
  if (unknown.length > 0) throw new Error(`categories missing from CATEGORY_ORDER: ${unknown.join(', ')}`)
  const sections = CATEGORY_ORDER.flatMap((category) => {
    const entries = tools.filter((tool) => tool.category === category)
    return entries.length === 0 ? [] : [`### ${category}`, '', ...entries.map(entry), '']
  })
  return `${START}\n\n${sections.join('\n').trimEnd()}\n\n${END}`
}

export function update(readme: string, tools: Tool[]): string {
  const start = readme.indexOf(START)
  const end = readme.indexOf(END)
  if (start === -1 || end === -1) throw new Error(`README.md needs ${START} and ${END} markers`)
  return readme.slice(0, start) + render(tools) + readme.slice(end + END.length)
}

if (import.meta.main) {
  const current = readFileSync('README.md', 'utf8')
  const next = update(current, readTools())
  if (process.argv.includes('--check')) {
    if (next !== current) {
      console.error('README.md is out of date: run `pnpm run readme` and commit the result.')
      process.exit(1)
    }
    console.log('README.md is up to date')
  } else {
    writeFileSync('README.md', next)
  }
}
