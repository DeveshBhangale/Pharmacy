import React, { useState } from 'react';
import {
    Notifications as NotificationsIcon,
    Security as SecurityIcon,
    Store as StoreIcon,
    Payment as PaymentIcon,
    Email as EmailIcon,
    Language as LanguageIcon
} from '@mui/icons-material';

interface SettingsSection {
    id: string;
    title: string;
    icon: JSX.Element;
    fields: {
        id: string;
        label: string;
        type: 'text' | 'email' | 'select' | 'switch' | 'textarea';
        value: string | boolean;
        options?: string[];
    }[];
}

const Settings: React.FC = () => {
    const [activeSection, setActiveSection] = useState('store');
    const [settings] = useState<SettingsSection[]>([
        {
            id: 'store',
            title: 'Store Settings',
            icon: <StoreIcon />,
            fields: [
                {
                    id: 'storeName',
                    label: 'Store Name',
                    type: 'text',
                    value: 'PMS Pharmacy'
                },
                {
                    id: 'storeAddress',
                    label: 'Store Address',
                    type: 'textarea',
                    value: '123 Healthcare Street, Medical District, City - 123456'
                },
                {
                    id: 'storePhone',
                    label: 'Store Phone',
                    type: 'text',
                    value: '+91 1234567890'
                }
            ]
        },
        {
            id: 'notifications',
            title: 'Notifications',
            icon: <NotificationsIcon />,
            fields: [
                {
                    id: 'emailNotifications',
                    label: 'Email Notifications',
                    type: 'switch',
                    value: true
                },
                {
                    id: 'orderUpdates',
                    label: 'Order Updates',
                    type: 'switch',
                    value: true
                },
                {
                    id: 'stockAlerts',
                    label: 'Low Stock Alerts',
                    type: 'switch',
                    value: true
                }
            ]
        },
        {
            id: 'security',
            title: 'Security',
            icon: <SecurityIcon />,
            fields: [
                {
                    id: 'twoFactor',
                    label: 'Two-Factor Authentication',
                    type: 'switch',
                    value: false
                },
                {
                    id: 'sessionTimeout',
                    label: 'Session Timeout (minutes)',
                    type: 'select',
                    value: '30',
                    options: ['15', '30', '60', '120']
                }
            ]
        },
        {
            id: 'payment',
            title: 'Payment',
            icon: <PaymentIcon />,
            fields: [
                {
                    id: 'currency',
                    label: 'Currency',
                    type: 'select',
                    value: 'INR',
                    options: ['INR', 'USD', 'EUR', 'GBP']
                },
                {
                    id: 'paymentMethods',
                    label: 'Payment Methods',
                    type: 'select',
                    value: 'all',
                    options: ['all', 'card_only', 'cash_only']
                }
            ]
        },
        {
            id: 'email',
            title: 'Email Settings',
            icon: <EmailIcon />,
            fields: [
                {
                    id: 'emailFrom',
                    label: 'From Email',
                    type: 'email',
                    value: 'noreply@pmspharmacy.com'
                },
                {
                    id: 'emailTemplate',
                    label: 'Email Template',
                    type: 'select',
                    value: 'default',
                    options: ['default', 'minimal', 'branded']
                }
            ]
        },
        {
            id: 'localization',
            title: 'Localization',
            icon: <LanguageIcon />,
            fields: [
                {
                    id: 'language',
                    label: 'Language',
                    type: 'select',
                    value: 'en',
                    options: ['en', 'hi', 'es', 'fr']
                },
                {
                    id: 'timeZone',
                    label: 'Time Zone',
                    type: 'select',
                    value: 'Asia/Kolkata',
                    options: ['Asia/Kolkata', 'UTC', 'America/New_York', 'Europe/London']
                }
            ]
        }
    ]);

    const handleSave = () => {
        // TODO: Implement settings save functionality
        console.log('Settings saved');
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold text-amazon-dark">Settings</h1>
                <button
                    onClick={handleSave}
                    className="bg-amazon-orange text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-amazon-orange-hover"
                >
                    Save Changes
                </button>
            </div>

            <div className="grid grid-cols-12 gap-6">
                {/* Settings Navigation */}
                <div className="col-span-3">
                    <div className="bg-white rounded-lg shadow-md overflow-hidden">
                        <nav className="space-y-1">
                            {settings.map((section) => (
                                <button
                                    key={section.id}
                                    onClick={() => setActiveSection(section.id)}
                                    className={`w-full flex items-center px-4 py-3 text-sm font-medium ${activeSection === section.id
                                        ? 'bg-amazon-orange text-white'
                                        : 'text-gray-600 hover:bg-gray-50'
                                        }`}
                                >
                                    <span className="mr-3">{section.icon}</span>
                                    {section.title}
                                </button>
                            ))}
                        </nav>
                    </div>
                </div>

                {/* Settings Content */}
                <div className="col-span-9">
                    <div className="bg-white rounded-lg shadow-md p-6">
                        {settings.map((section) => (
                            <div
                                key={section.id}
                                className={`space-y-6 ${activeSection === section.id ? '' : 'hidden'}`}
                            >
                                <h2 className="text-xl font-semibold text-amazon-dark">{section.title}</h2>
                                <div className="space-y-4">
                                    {section.fields.map((field) => (
                                        <div key={field.id} className="grid grid-cols-3 items-center gap-4">
                                            <label htmlFor={field.id} className="text-sm font-medium text-gray-700">
                                                {field.label}
                                            </label>
                                            <div className="col-span-2">
                                                {field.type === 'switch' ? (
                                                    <div className="flex items-center">
                                                        <button
                                                            type="button"
                                                            className={`relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none ${field.value ? 'bg-amazon-orange' : 'bg-gray-200'
                                                                }`}
                                                            role="switch"
                                                            aria-checked={Boolean(field.value)}
                                                        >
                                                            <span
                                                                className={`pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out ${field.value ? 'translate-x-5' : 'translate-x-0'
                                                                    }`}
                                                            />
                                                        </button>
                                                    </div>
                                                ) : field.type === 'select' ? (
                                                    <select
                                                        id={field.id}
                                                        value={field.value as string}
                                                        className="mt-1 block w-full rounded-md border-gray-300 py-2 pl-3 pr-10 text-base focus:border-amazon-orange focus:outline-none focus:ring-amazon-orange sm:text-sm"
                                                    >
                                                        {field.options?.map((option) => (
                                                            <option key={option} value={option}>
                                                                {option}
                                                            </option>
                                                        ))}
                                                    </select>
                                                ) : field.type === 'textarea' ? (
                                                    <textarea
                                                        id={field.id}
                                                        rows={3}
                                                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-amazon-orange focus:ring-amazon-orange sm:text-sm"
                                                        defaultValue={field.value as string}
                                                    />
                                                ) : (
                                                    <input
                                                        type={field.type}
                                                        id={field.id}
                                                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-amazon-orange focus:ring-amazon-orange sm:text-sm"
                                                        defaultValue={field.value as string}
                                                    />
                                                )}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Settings; 