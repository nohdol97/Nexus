"use client";

import { useState } from "react";
import { ChatInterface } from "@/components/playground/ChatInterface";
import { ModelSelector } from "@/components/playground/ModelSelector";
import { Sliders } from "lucide-react";

export default function PlaygroundPage() {
    const [model, setModel] = useState("llama-3-8b");
    const [temperature, setTemperature] = useState(0.7);
    const [maxTokens, setMaxTokens] = useState(1024);

    return (
        <div className="flex flex-col h-full p-6 space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold tracking-tight text-gray-900 dark:text-gray-100">Playground</h1>
                    <p className="text-muted-foreground text-gray-500 dark:text-gray-400">
                        Test and interact with your deployed models
                    </p>
                </div>
                <div className="w-64">
                    <ModelSelector value={model} onChange={setModel} />
                </div>
            </div>

            <div className="flex gap-6 h-full">
                <div className="flex-1">
                    <ChatInterface />
                </div>

                <div className="w-80 space-y-6 rounded-xl border border-gray-200 bg-white p-6 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
                    <div className="flex items-center gap-2 pb-2 border-b border-gray-100 dark:border-zinc-800">
                        <Sliders className="h-4 w-4 text-gray-500" />
                        <h2 className="font-semibold text-gray-900 dark:text-gray-100">Parameters</h2>
                    </div>

                    <div className="space-y-4">
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-gray-700 dark:text-gray-300 flex justify-between">
                                <span>Temperature</span>
                                <span className="text-gray-500">{temperature}</span>
                            </label>
                            <input
                                type="range"
                                min="0"
                                max="2"
                                step="0.1"
                                value={temperature}
                                onChange={(e) => setTemperature(parseFloat(e.target.value))}
                                className="w-full accent-indigo-600"
                            />
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium text-gray-700 dark:text-gray-300 flex justify-between">
                                <span>Max Tokens</span>
                                <span className="text-gray-500">{maxTokens}</span>
                            </label>
                            <input
                                type="range"
                                min="1"
                                max="4096"
                                step="1"
                                value={maxTokens}
                                onChange={(e) => setMaxTokens(parseInt(e.target.value))}
                                className="w-full accent-indigo-600"
                            />
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium text-gray-700 dark:text-gray-300 flex justify-between">
                                <span>Top P</span>
                                <span className="text-gray-500">0.9</span>
                            </label>
                            <input
                                type="range"
                                min="0"
                                max="1"
                                step="0.1"
                                value={0.9}
                                className="w-full accent-indigo-600"
                                disabled
                            />
                        </div>
                    </div>

                    <div className="pt-4 mt-auto">
                        <div className="p-3 rounded-lg bg-gray-50 dark:bg-zinc-800/50 text-xs text-gray-500 dark:text-gray-400">
                            <p>Note: Parameters are simulated in this UI demo.</p>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    );
}
