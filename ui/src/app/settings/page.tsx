"use client";

import { Save, AlertTriangle, RefreshCw } from "lucide-react";

export default function SettingsPage() {
    return (
        <div className="p-8 max-w-4xl space-y-8">
            <div>
                <h1 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-gray-100">Settings</h1>
                <p className="text-muted-foreground text-gray-500 dark:text-gray-400 mt-2">
                    Configure Nexus Gateway parameters and system behavior
                </p>
            </div>

            <div className="space-y-6">
                {/* Routing Configuration */}
                <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
                    <div className="flex items-center gap-2 mb-6">
                        <RefreshCw className="h-5 w-5 text-indigo-500" />
                        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Model Routing</h2>
                    </div>

                    <div className="space-y-4">
                        <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Default Model</label>
                                <select className="w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 dark:border-zinc-800 dark:bg-zinc-900">
                                    <option>Llama 3 8B</option>
                                    <option>Mistral 7B</option>
                                </select>
                                <p className="text-xs text-gray-500">Model used when no specific model is requested</p>
                            </div>

                            <div className="space-y-2">
                                <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Fallback Strategy</label>
                                <select className="w-full rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 dark:border-zinc-800 dark:bg-zinc-900">
                                    <option>Log & Fail</option>
                                    <option>Switch to Backup Model</option>
                                    <option>Queue Request</option>
                                </select>
                                <p className="text-xs text-gray-500">Action taken when primary model is unavailable</p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Circuit Breaker */}
                <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
                    <div className="flex items-center gap-2 mb-6">
                        <AlertTriangle className="h-5 w-5 text-orange-500" />
                        <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Circuit Breaker</h2>
                    </div>

                    <div className="space-y-4">
                        <div className="flex items-center justify-between py-3">
                            <div>
                                <label className="text-sm font-medium text-gray-900 dark:text-gray-100">Enable Circuit Breaker</label>
                                <p className="text-xs text-gray-500 dark:text-gray-400">Automatically stop traffic to failing services</p>
                            </div>
                            <input type="checkbox" defaultChecked className="h-5 w-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 accent-indigo-600" />
                        </div>

                        <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-100 dark:border-zinc-800">
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Failure Threshold</label>
                                <div className="flex items-center gap-2">
                                    <input type="number" defaultValue={5} className="w-20 rounded-lg border border-gray-200 px-3 py-1 text-sm dark:border-zinc-800 dark:bg-zinc-900" />
                                    <span className="text-sm text-gray-500">errors / minute</span>
                                </div>
                            </div>
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Reset Timeout</label>
                                <div className="flex items-center gap-2">
                                    <input type="number" defaultValue={30} className="w-20 rounded-lg border border-gray-200 px-3 py-1 text-sm dark:border-zinc-800 dark:bg-zinc-900" />
                                    <span className="text-sm text-gray-500">seconds</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="flex justify-end pt-4">
                    <button className="flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 transition-colors shadow-sm">
                        <Save className="h-4 w-4" />
                        Save Changes
                    </button>
                </div>
            </div>
        </div>
    );
}
