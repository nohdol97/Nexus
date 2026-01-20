import { LucideIcon } from "lucide-react";
import { cn } from "@/lib/utils";

interface StatsCardProps {
    title: string;
    value: string;
    change?: string;
    icon: LucideIcon;
    trend?: "up" | "down" | "neutral";
}

export function StatsCard({ title, value, change, icon: Icon, trend }: StatsCardProps) {
    return (
        <div className="rounded-xl border bg-card text-card-foreground shadow-sm p-6 bg-white dark:bg-zinc-900 border-gray-200 dark:border-zinc-800">
            <div className="flex items-center justify-between space-y-0 pb-2">
                <h3 className="tracking-tight text-sm font-medium text-muted-foreground text-gray-500 dark:text-gray-400">
                    {title}
                </h3>
                <Icon className="h-4 w-4 text-muted-foreground text-gray-500 dark:text-gray-400" />
            </div>
            <div className="text-2xl font-bold text-gray-900 dark:text-gray-100">{value}</div>
            {change && (
                <p className={cn("text-xs flex items-center mt-1",
                    trend === "up" ? "text-green-500" : trend === "down" ? "text-red-500" : "text-gray-500"
                )}>
                    {change}
                </p>
            )}
        </div>
    );
}
