import React from 'react';
import {
    People as UsersIcon,
    ShoppingCart as OrdersIcon,
    AttachMoney as RevenueIcon,
    LocalPharmacy as MedicinesIcon,
} from '@mui/icons-material';

const StatCard: React.FC<{
    title: string;
    value: string | number;
    icon: React.ReactNode;
    trend?: string;
}> = ({ title, value, icon, trend }) => (
    <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6">
        <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-700">{title}</h3>
            <div className="text-amazon-orange">{icon}</div>
        </div>
        <div className="flex items-baseline">
            <p className="text-3xl font-bold text-amazon-dark">{value}</p>
            {trend && (
                <span className="ml-2 text-sm text-green-600">
                    {trend}
                </span>
            )}
        </div>
    </div>
);

const Dashboard: React.FC = () => {
    // TODO: Replace with actual data from API
    const stats = [
        {
            title: 'Total Users',
            value: '1,234',
            icon: <UsersIcon className="w-8 h-8" />,
            trend: '+12% from last month',
        },
        {
            title: 'Total Orders',
            value: '456',
            icon: <OrdersIcon className="w-8 h-8" />,
            trend: '+8% from last month',
        },
        {
            title: 'Total Revenue',
            value: '₹12,345',
            icon: <RevenueIcon className="w-8 h-8" />,
            trend: '+15% from last month',
        },
        {
            title: 'Total Medicines',
            value: '789',
            icon: <MedicinesIcon className="w-8 h-8" />,
            trend: '+5% from last month',
        },
    ];

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <h1 className="text-2xl font-bold text-amazon-dark">Dashboard Overview</h1>
            </div>
            <div id="dashboard-content" className="space-y-6">
                <div className="flex items-center justify-between">
                    <h1 className="text-2xl font-bold text-amazon-dark">Dashboard Overview</h1>
                    <div className="flex space-x-4">
                        <select className="bg-white border border-gray-300 rounded-md px-4 py-2 text-sm">
                            <option>Last 7 days</option>
                            <option>Last 30 days</option>
                            <option>Last 90 days</option>
                        </select>
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {stats.map((stat) => (
                        <StatCard key={stat.title} {...stat} />
                    ))}
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Recent Orders */}
                    <div className="bg-white rounded-lg shadow-md p-6">
                        <h2 className="text-xl font-semibold text-amazon-dark mb-4">Recent Orders</h2>
                        <div className="space-y-4">
                            {[1, 2, 3, 4, 5].map((order) => (
                                <div key={order} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                                    <div>
                                        <p className="font-medium">Order #{order}</p>
                                        <p className="text-sm text-gray-500">2 items • ₹1,234</p>
                                    </div>
                                    <span className="px-3 py-1 text-sm rounded-full bg-green-100 text-green-800">
                                        Delivered
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Low Stock Medicines */}
                    <div className="bg-white rounded-lg shadow-md p-6">
                        <h2 className="text-xl font-semibold text-amazon-dark mb-4">Low Stock Medicines</h2>
                        <div className="space-y-4">
                            {[1, 2, 3, 4, 5].map((medicine) => (
                                <div key={medicine} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                                    <div>
                                        <p className="font-medium">Medicine {medicine}</p>
                                        <p className="text-sm text-gray-500">Category • ₹299</p>
                                    </div>
                                    <span className="px-3 py-1 text-sm rounded-full bg-red-100 text-red-800">
                                        5 units left
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard; 