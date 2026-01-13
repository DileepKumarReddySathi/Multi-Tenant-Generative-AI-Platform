import Link from "next/link";
import { Button } from "@/components/ui/button";
import { MessageSquare, Bot, Settings, LayoutDashboard } from "lucide-react";

export default function TenantLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="flex min-h-screen">
            {/* Sidebar */}
            <aside className="w-64 border-r bg-muted/40 hidden md:block">
                <div className="flex h-16 items-center border-b px-6 font-semibold">
                    Tenant Portal
                </div>
                <nav className="flex flex-col gap-2 p-4">
                    <Link href="/tenant">
                        <Button variant="ghost" className="w-full justify-start gap-2">
                            <LayoutDashboard className="h-4 w-4" />
                            Dashboard
                        </Button>
                    </Link>
                    <Link href="/tenant/chat">
                        <Button variant="ghost" className="w-full justify-start gap-2">
                            <MessageSquare className="h-4 w-4" />
                            AI Chat (RAG)
                        </Button>
                    </Link>
                    <Link href="/tenant/agents">
                        <Button variant="ghost" className="w-full justify-start gap-2">
                            <Bot className="h-4 w-4" />
                            Agent Builder
                        </Button>
                    </Link>
                    <Link href="/tenant/settings">
                        <Button variant="ghost" className="w-full justify-start gap-2">
                            <Settings className="h-4 w-4" />
                            Settings
                        </Button>
                    </Link>
                </nav>
            </aside>

            {/* Main Content */}
            <div className="flex-1 flex flex-col">
                <header className="flex h-16 items-center gap-4 border-b bg-background px-6">
                    <h1 className="text-lg font-semibold">Workspace / Default</h1>
                    <div className="ml-auto">
                        <Button size="sm" variant="outline">Docs</Button>
                    </div>
                </header>
                <main className="flex-1 p-6 overflow-auto">
                    {children}
                </main>
            </div>
        </div>
    );
}
