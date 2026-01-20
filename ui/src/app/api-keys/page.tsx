import { ApiKeyList } from "@/components/apikeys/ApiKeyList";
import { Plus } from "lucide-react";

export default function ApiKeysPage() {
    return (
        <div className="p-8 space-y-8">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-gray-100">API Keys</h1>
                    <p className="text-muted-foreground text-gray-500 dark:text-gray-400 mt-2">
                        Manage your API keys for accessing Nexus Gateway
                    </p>
                </div>
                <button className="flex items-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 transition-colors">
                    <Plus className="h-4 w-4" />
                    Create New Key
                </button>
            </div>

            <ApiKeyList />

            <div className="rounded-lg border border-yellow-200 bg-yellow-50 p-4 dark:border-yellow-900/50 dark:bg-yellow-900/20">
                <div className="flex">
                    <div className="ml-3">
                        <h3 className="text-sm font-medium text-yellow-800 dark:text-yellow-200">Security Notice</h3>
                        <div className="mt-2 text-sm text-yellow-700 dark:text-yellow-300">
                            <p>
                                API keys grant full access to your models. Never share these keys on client-side code (browsers, mobile apps).
                                Use them only from secure backend environments.
                            </p>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    );
}
