"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
    LayoutDashboard,
    Play,
    Key,
    Settings,
    BrainCircuit,
    BarChart3,
} from "lucide-react";

const navigation = [
    { name: "Dashboard", href: "/", icon: LayoutDashboard, external: false },
    { name: "Playground", href: "/playground", icon: Play, external: false },
    { name: "API Keys", href: "/api-keys", icon: Key, external: false },
    { name: "Settings", href: "/settings", icon: Settings, external: false },
    {
        name: "Grafana",
        href: "http://localhost:3000/d/nexus-gateway/nexus-gateway",
        icon: BarChart3,
        external: true,
    },
];

export function Sidebar() {
    const pathname = usePathname();

    return (
        <div className="flex h-screen w-64 flex-col border-r bg-gray-50 dark:bg-zinc-900 border-gray-200 dark:border-zinc-800">
            <div className="flex items-center gap-2 px-6 py-8">
                <BrainCircuit className="h-8 w-8 text-indigo-600 dark:text-indigo-400" />
                <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-violet-600 dark:from-indigo-400 dark:to-violet-400">
                    Nexus
                </span>
            </div>

            <nav className="flex flex-1 flex-col px-4 space-y-1">
                {navigation.map((item) => {
                    const isActive = !item.external && pathname === item.href;
                    const className = cn(
                        "group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-200",
                        isActive
                            ? "bg-indigo-50 text-indigo-700 dark:bg-indigo-900/20 dark:text-indigo-300"
                            : "text-gray-700 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-zinc-800/50 hover:text-gray-900 dark:hover:text-gray-200"
                    );
                    const iconClassName = cn(
                        "h-5 w-5 transition-colors",
                        isActive
                            ? "text-indigo-600 dark:text-indigo-400"
                            : "text-gray-400 group-hover:text-gray-600 dark:text-gray-500 dark:group-hover:text-gray-300"
                    );

                    if (item.external) {
                        return (
                            <a
                                key={item.name}
                                href={item.href}
                                target="_blank"
                                rel="noreferrer noopener"
                                className={className}
                            >
                                <item.icon className={iconClassName} />
                                {item.name}
                            </a>
                        );
                    }

                    return (
                        <Link key={item.name} href={item.href} className={className}>
                            <item.icon className={iconClassName} />
                            {item.name}
                        </Link>
                    );
                })}
            </nav>

            <div className="p-4 border-t border-gray-200 dark:border-zinc-800">
                <div className="flex items-center gap-3 px-3 py-2 rounded-lg bg-gray-100 dark:bg-zinc-800">
                    <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
                    <div className="flex flex-col">
                        <span className="text-xs font-medium text-gray-900 dark:text-gray-200">
                            System Online
                        </span>
                        <span className="text-[10px] text-gray-500 dark:text-gray-400">
                            v1.0.0
                        </span>
                    </div>
                </div>
            </div>
        </div>
    );
}
