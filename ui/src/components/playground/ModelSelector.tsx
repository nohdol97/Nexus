import { ChevronDown } from "lucide-react";

interface ModelSelectorProps {
    value: string;
    onChange: (value: string) => void;
}

export function ModelSelector({ value, onChange }: ModelSelectorProps) {
    return (
        <div className="relative">
            <select
                value={value}
                onChange={(e) => onChange(e.target.value)}
                className="w-full appearance-none rounded-lg border border-gray-200 bg-white px-4 py-2 pr-8 text-sm font-medium text-gray-900 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-zinc-800 dark:bg-zinc-900 dark:text-gray-100"
            >
                <option value="llama-3-8b">Llama 3 8B</option>
                <option value="mistral-7b">Mistral 7B</option>
                <option value="gpt-4">GPT-4 (Proxy)</option>
                <option value="claude-3-sonnet">Claude 3.5 Sonnet (Proxy)</option>
            </select>
            <ChevronDown className="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-500" />
        </div>
    );
}
