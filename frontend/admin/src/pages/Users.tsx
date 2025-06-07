import React, { useState } from 'react';
import { Block, CheckCircle, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';

interface User {
    id: string;
    name: string;
    email: string;
    joinDate: string;
    status: 'active' | 'inactive';
    orders: number;
    totalSpent: number;
}

const Users: React.FC = () => {
    // TODO: Replace with actual API call
    const [users] = useState<User[]>([
        {
            id: 'USR001',
            name: 'John Doe',
            email: 'john.doe@example.com',
            joinDate: '2024-01-15',
            status: 'active',
            orders: 12,
            totalSpent: 15999.99
        },
        {
            id: 'USR002',
            name: 'Jane Smith',
            email: 'jane.smith@example.com',
            joinDate: '2024-01-20',
            status: 'active',
            orders: 8,
            totalSpent: 8999.99
        },
        {
            id: 'USR003',
            name: 'Mike Johnson',
            email: 'mike.j@example.com',
            joinDate: '2024-01-25',
            status: 'inactive',
            orders: 3,
            totalSpent: 2499.99
        },
        {
            id: 'USR004',
            name: 'Sarah Williams',
            email: 'sarah.w@example.com',
            joinDate: '2024-02-01',
            status: 'active',
            orders: 5,
            totalSpent: 5999.99
        }
    ]);

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold text-amazon-dark">Users</h1>
                <div className="flex space-x-4">
                    <select className="bg-white border border-gray-300 rounded-md px-4 py-2 text-sm">
                        <option>All Users</option>
                        <option>Active</option>
                        <option>Inactive</option>
                    </select>
                    <input
                        type="text"
                        placeholder="Search users..."
                        className="border border-gray-300 rounded-md px-4 py-2 text-sm"
                    />
                </div>
            </div>

            <div className="bg-white shadow-md rounded-lg overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                User
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Email
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Join Date
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Status
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Orders
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Total Spent
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Actions
                            </th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {users.map((user) => (
                            <tr key={user.id} className="hover:bg-gray-50">
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <div className="flex items-center">
                                        <div className="flex-shrink-0 h-10 w-10">
                                            <div className="h-10 w-10 rounded-full bg-amazon-dark text-white flex items-center justify-center text-lg font-semibold">
                                                {user.name.charAt(0)}
                                            </div>
                                        </div>
                                        <div className="ml-4">
                                            <div className="text-sm font-medium text-amazon-dark">{user.name}</div>
                                            <div className="text-sm text-gray-500">ID: {user.id}</div>
                                        </div>
                                    </div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {user.email}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {user.joinDate}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <div className="flex items-center">
                                        {user.status === 'active' ? (
                                            <CheckCircle className="text-green-500 mr-2" />
                                        ) : (
                                            <Block className="text-red-500 mr-2" />
                                        )}
                                        <span
                                            className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${user.status === 'active'
                                                ? 'bg-green-100 text-green-800'
                                                : 'bg-red-100 text-red-800'
                                                }`}
                                        >
                                            {user.status.charAt(0).toUpperCase() + user.status.slice(1)}
                                        </span>
                                    </div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {user.orders}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    ₹{user.totalSpent.toFixed(2)}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    <div className="flex space-x-2">
                                        <button className="text-blue-500 hover:text-blue-700">
                                            <EditIcon className="w-5 h-5" />
                                        </button>
                                        <button className="text-red-500 hover:text-red-700">
                                            <DeleteIcon className="w-5 h-5" />
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="flex justify-between items-center">
                <div className="text-sm text-gray-500">
                    Showing 1 to 4 of 4 users
                </div>
                <div className="flex space-x-2">
                    <button className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50">
                        Previous
                    </button>
                    <button className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50">
                        Next
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Users; 