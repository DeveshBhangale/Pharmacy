import React, { useState } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import {
    Menu as MenuIcon,
    Dashboard as DashboardIcon,
    People as PeopleIcon,
    Settings as SettingsIcon,
    Logout as LogoutIcon,
    ShoppingCart as OrdersIcon,
    LocalPharmacy as MedicinesIcon,
} from '@mui/icons-material';

const Layout: React.FC = () => {
    const [mobileOpen, setMobileOpen] = useState(false);
    const navigate = useNavigate();

    const handleDrawerToggle = () => {
        setMobileOpen(!mobileOpen);
    };

    const menuItems = [
        { text: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
        { text: 'Orders', icon: <OrdersIcon />, path: '/orders' },
        { text: 'Medicines', icon: <MedicinesIcon />, path: '/medicines' },
        { text: 'Users', icon: <PeopleIcon />, path: '/users' },
        { text: 'Settings', icon: <SettingsIcon />, path: '/settings' },
    ];

    return (
        <div className="min-h-screen bg-gray-100">
            {/* Header */}
            <header className="bg-amazon-dark text-white shadow-lg">
                <div className="max-w-7xl mx-auto px-4">
                    <div className="flex items-center justify-between h-16">
                        <div className="flex items-center">
                            <button
                                onClick={handleDrawerToggle}
                                className="p-2 rounded-md hover:bg-amazon-gray lg:hidden"
                            >
                                <MenuIcon />
                            </button>
                            <span className="text-xl font-bold ml-4">Admin Dashboard</span>
                        </div>
                        <div className="flex items-center">
                            <button
                                onClick={() => navigate('/login')}
                                className="flex items-center px-4 py-2 rounded-md hover:bg-amazon-gray"
                            >
                                <LogoutIcon className="mr-2" />
                                Logout
                            </button>
                        </div>
                    </div>
                </div>
            </header>

            <div className="flex">
                {/* Sidebar */}
                <aside
                    className={`fixed inset-y-0 left-0 transform ${mobileOpen ? 'translate-x-0' : '-translate-x-full'
                        } lg:translate-x-0 lg:static lg:inset-0 z-30 w-64 bg-white shadow-lg transition-transform duration-300 ease-in-out`}
                >
                    <div className="h-full pt-16 pb-4 overflow-y-auto">
                        <nav className="mt-5 px-2">
                            {menuItems.map((item) => (
                                <button
                                    key={item.text}
                                    onClick={() => navigate(item.path)}
                                    className="group flex items-center px-4 py-3 text-gray-700 hover:bg-amazon-orange hover:text-white rounded-md w-full transition-colors duration-200"
                                >
                                    <span className="mr-3">{item.icon}</span>
                                    {item.text}
                                </button>
                            ))}
                        </nav>
                    </div>
                </aside>

                {/* Main Content */}
                <main className="flex-1 p-6 lg:ml-64">
                    <div className="max-w-7xl mx-auto">
                        <Outlet />
                    </div>
                </main>
            </div>

            {/* Mobile Overlay */}
            {mobileOpen && (
                <div
                    className="fixed inset-0 bg-black bg-opacity-50 z-20 lg:hidden"
                    onClick={handleDrawerToggle}
                />
            )}
        </div>
    );
};

export default Layout; 