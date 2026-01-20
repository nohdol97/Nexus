"use client";

import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const data = [
    { time: "00:00", requests: 400 },
    { time: "04:00", requests: 300 },
    { time: "08:00", requests: 1200 },
    { time: "12:00", requests: 2400 },
    { time: "16:00", requests: 1800 },
    { time: "20:00", requests: 800 },
    { time: "23:59", requests: 500 },
];

export function RequestsChart() {
    return (
        <div className="h-[350px] w-full rounded-xl border bg-card p-6 shadow-sm bg-white dark:bg-zinc-900 border-gray-200 dark:border-zinc-800">
            <div className="mb-6">
                <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100">
                    Request Volume
                </h3>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                    Total API requests over time
                </p>
            </div>
            <div className="h-[250px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={data}>
                        <defs>
                            <linearGradient id="colorRequests" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#4f46e5" stopOpacity={0.3} />
                                <stop offset="95%" stopColor="#4f46e5" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" className="stroke-gray-200 dark:stroke-zinc-800" vertical={false} />
                        <XAxis
                            dataKey="time"
                            stroke="#888888"
                            fontSize={12}
                            tickLine={false}
                            axisLine={false}
                        />
                        <YAxis
                            stroke="#888888"
                            fontSize={12}
                            tickLine={false}
                            axisLine={false}
                            tickFormatter={(value) => `${value}`}
                        />
                        <Tooltip
                            contentStyle={{
                                backgroundColor: 'var(--color-background)',
                                borderColor: 'var(--color-border)',
                                borderRadius: '8px'
                            }}
                        />
                        <Area
                            type="monotone"
                            dataKey="requests"
                            stroke="#4f46e5"
                            strokeWidth={2}
                            fillOpacity={1}
                            fill="url(#colorRequests)"
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}
