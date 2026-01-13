import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowUpRight } from "lucide-react";

export default function TenantDashboard() {
    return (
        <div className="space-y-6">
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                <Card className="p-6">
                    <h3 className="font-semibold leading-none tracking-tight">API Usage</h3>
                    <p className="text-sm text-muted-foreground mt-2">1,234 requests this month</p>
                    <div className="mt-4 h-2 bg-secondary rounded-full overflow-hidden">
                        <div className="h-full bg-primary w-[45%]"></div>
                    </div>
                </Card>

                <Card className="p-6">
                    <h3 className="font-semibold leading-none tracking-tight">Vector Storage</h3>
                    <p className="text-sm text-muted-foreground mt-2">450 documents indexed</p>
                    <div className="mt-4 h-2 bg-secondary rounded-full overflow-hidden">
                        <div className="h-full bg-green-500 w-[12%]"></div>
                    </div>
                </Card>

                <Card className="p-6">
                    <h3 className="font-semibold leading-none tracking-tight">Agent Runs</h3>
                    <p className="text-sm text-muted-foreground mt-2">89 active sessions</p>
                </Card>
            </div>

            <div className="grid gap-6 md:grid-cols-2">
                <Card className="p-6">
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="font-semibold">Recent Documents</h3>
                        <Button variant="ghost" size="sm">View All</Button>
                    </div>
                    <div className="space-y-2">
                        {['Q3 Financials.pdf', 'Engineering Onboarding.docx', 'Product Roadmap 2024.md'].map((doc, i) => (
                            <div key={i} className="flex items-center justify-between p-2 rounded-lg hover:bg-muted/50 transition-colors">
                                <span className="text-sm text-foreground/80">{doc}</span>
                                <span className="text-xs text-muted-foreground">Just now</span>
                            </div>
                        ))}
                    </div>
                </Card>

                <Card className="p-6 flex flex-col items-center justify-center text-center space-y-4 border-dashed">
                    <div className="p-3 bg-primary/10 rounded-full text-primary">
                        <ArrowUpRight className="h-6 w-6" />
                    </div>
                    <div>
                        <h3 className="font-semibold">Start a new project</h3>
                        <p className="text-sm text-muted-foreground max-w-xs mx-auto">Create a custom agent or fine-tune a model on your data.</p>
                    </div>
                    <Button>Create Agent</Button>
                </Card>
            </div>
        </div>
    );
}
