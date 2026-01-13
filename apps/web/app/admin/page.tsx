import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card"; // Need to create Card component
import { Users, Activity, CreditCard, Settings } from "lucide-react";

export default function AdminDashboard() {
    return (
        <div className="flex min-h-screen flex-col">
            <header className="sticky top-0 z-30 flex h-16 items-center gap-4 border-b bg-background px-6">
                <h1 className="text-lg font-semibold md:text-xl">Platform Admin</h1>
                <div className="ml-auto flex items-center gap-4">
                    <Button size="sm" variant="outline">Logout</Button>
                </div>
            </header>
            <main className="flex flex-1 flex-col gap-8 p-8 md:p-10">
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                    <div className="rounded-xl border bg-card text-card-foreground shadow p-6">
                        <div className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <h3 className="tracking-tight text-sm font-medium">Total Tenants</h3>
                            <Users className="h-4 w-4 text-muted-foreground" />
                        </div>
                        <div className="text-2xl font-bold">12</div>
                        <p className="text-xs text-muted-foreground">+2 from last month</p>
                    </div>
                    <div className="rounded-xl border bg-card text-card-foreground shadow p-6">
                        <div className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <h3 className="tracking-tight text-sm font-medium">Active Agents</h3>
                            <Activity className="h-4 w-4 text-muted-foreground" />
                        </div>
                        <div className="text-2xl font-bold">345</div>
                        <p className="text-xs text-muted-foreground">+12% activity</p>
                    </div>
                    <div className="rounded-xl border bg-card text-card-foreground shadow p-6">
                        <div className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <h3 className="tracking-tight text-sm font-medium">Revenue</h3>
                            <CreditCard className="h-4 w-4 text-muted-foreground" />
                        </div>
                        <div className="text-2xl font-bold">$12,234</div>
                        <p className="text-xs text-muted-foreground">+5% from last month</p>
                    </div>
                </div>

                <div>
                    <h2 className="text-2xl font-bold tracking-tight mb-4">Recent Tenants</h2>
                    <div className="rounded-md border">
                        <div className="p-4">
                            <div className="grid grid-cols-4 font-medium text-muted-foreground mb-4">
                                <div>ID</div>
                                <div>Name</div>
                                <div>Plan</div>
                                <div>Status</div>
                            </div>
                            {/* Mock Data */}
                            {[1, 2, 3].map((i) => (
                                <div key={i} className="grid grid-cols-4 py-4 border-t items-center">
                                    <div className="text-sm">tenant-{i}</div>
                                    <div className="text-sm">Acme Corp {i}</div>
                                    <div className="text-sm"><span className="inline-flex items-center rounded-md bg-green-50 px-2 py-1 text-xs font-medium text-green-700 ring-1 ring-inset ring-green-600/20">Pro</span></div>
                                    <div className="text-sm">Active</div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
