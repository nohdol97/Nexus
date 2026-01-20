"use client";

import { Copy, Trash2, Eye, EyeOff } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

interface ApiKey {
    id: string;
    name: string;
    prefix: string;
    created: string;
    lastUsed: string;
    status: "active" | "revoked";
}

export function ApiKeyList() {
    const [keys] = useState<ApiKey[]>([
        {
            id: "1",
            name: "Production Key",
            prefix: "nx-prod-",
            created: "2024-03-10",
            lastUsed: "Just now",
            status: "active",
        },
        {
            id: "2",
            name: "Development Key",
            prefix: "nx-dev-",
            created: "2024-03-15",
            lastUsed: "2 hours ago",
            status: "active",
        },
        {
            id: "3",
            name: "Test Key (Old)",
            prefix: "nx-test-",
            created: "2024-01-01",
            lastUsed: "1 month ago",
            status: "revoked",
        },
    ]);

    const [visibleKeys, setVisibleKeys] = useState<Set<string>>(new Set());

    const toggleVisibility = (id: string) => {
        setVisibleKeys((prev) => {
            const next = new Set(prev);
            if (next.has(id)) {
                next.delete(id);
            } else {
                next.add(id);
            }
            return next;
        });
    };

    const copyToClipboard = (prefix: string) => {
        // In real app, we would copy the full key
        navigator.clipboard.writeText(prefix + "****************");
        alert("API Key copied to clipboard!");
    };

    return (
        <div className="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
            <table className="w-full text-left text-sm">
                <thead className="bg-gray-50 dark:bg-zinc-800/50">
                    <tr>
                        <th className="px-6 py-4 font-medium text-gray-900 dark:text-gray-100">Name</th>
                        <th className="px-6 py-4 font-medium text-gray-900 dark:text-gray-100">Token</th>
                        <th className="px-6 py-4 font-medium text-gray-900 dark:text-gray-100">Created</th>
                        <th className="px-6 py-4 font-medium text-gray-900 dark:text-gray-100">Last Used</th>
                        <th className="px-6 py-4 font-medium text-gray-900 dark:text-gray-100">Status</th>
                        <th className="px-6 py-4 font-medium text-gray-900 dark:text-gray-100 text-right">Actions</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-zinc-800">
                    {keys.map((key) => (
                        <tr key={key.id} className="hover:bg-gray-50 dark:hover:bg-zinc-800/50 transition-colors">
                            <td className="px-6 py-4 font-medium text-gray-900 dark:text-gray-100">{key.name}</td>
                            <td className="px-6 py-4 font-mono text-gray-500 dark:text-gray-400">
                                <div className="flex items-center gap-2">
                                    <span>{key.prefix}{visibleKeys.has(key.id) ? "8f92a3..." : "••••••••"}</span>
                                </div>
                            </td>
                            <td className="px-6 py-4 text-gray-500 dark:text-gray-400">{key.created}</td>
                            <td className="px-6 py-4 text-gray-500 dark:text-gray-400">{key.lastUsed}</td>
                            <td className="px-6 py-4">
                                <span
                                    className={cn(
                                        "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
                                        key.status === "active"
                                            ? "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400"
                                            : "bg-gray-100 text-gray-800 dark:bg-zinc-800 dark:text-gray-400"
                                    )}
                                >
                                    {key.status.charAt(0).toUpperCase() + key.status.slice(1)}
                                </span>
                            </td>
                            <td className="px-6 py-4 text-right">
                                <div className="flex items-center justify-end gap-2">
                                    <button
                                        onClick={() => toggleVisibility(key.id)}
                                        className="rounded-lg p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-600 dark:hover:bg-zinc-800 dark:hover:text-gray-300"
                                        title={visibleKeys.has(key.id) ? "Hide Key" : "Show Key"}
                                    >
                                        {visibleKeys.has(key.id) ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                                    </button>
                                    <button
                                        onClick={() => copyToClipboard(key.prefix)}
                                        className="rounded-lg p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-600 dark:hover:bg-zinc-800 dark:hover:text-gray-300"
                                        title="Copy Key"
                                    >
                                        <Copy className="h-4 w-4" />
                                    </button>
                                    <button
                                        className="rounded-lg p-2 text-gray-400 hover:bg-red-50 hover:text-red-600 dark:hover:bg-red-900/20 dark:hover:text-red-400"
                                        title="Revoke Key"
                                    >
                                        <Trash2 className="h-4 w-4" />
                                    </button>
                                </div>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
