import React, { useState } from 'react';
import { LocalShipping, CheckCircle, Warning, Block } from '@mui/icons-material';

interface Order {
    id: string;
    customerName: string;
    date: string;
    total: number;
    status: 'delivered' | 'processing' | 'cancelled' | 'pending';
    items: number;
}

const Orders: React.FC = () => {
    // TODO: Replace with actual API call
    const [orders] = useState<Order[]>([
        {
            id: 'ORD001',
            customerName: 'John Doe',
            date: '2024-02-20',
            total: 1299.99,
            status: 'delivered',
            items: 3
        },
        {
            id: 'ORD002',
            customerName: 'Jane Smith',
            date: '2024-02-19',
            total: 499.50,
            status: 'processing',
            items: 2
        },
        {
            id: 'ORD003',
            customerName: 'Mike Johnson',
            date: '2024-02-18',
            total: 799.99,
            status: 'pending',
            items: 1
        },
        {
            id: 'ORD004',
            customerName: 'Sarah Williams',
            date: '2024-02-17',
            total: 1599.99,
            status: 'cancelled',
            items: 4
        }
    ]);

    const getStatusIcon = (status: Order['status']) => {
        switch (status) {
            case 'delivered':
                return <CheckCircle className="text-green-500" />;
            case 'processing':
                return <LocalShipping className="text-blue-500" />;
            case 'cancelled':
                return <Block className="text-red-500" />;
            case 'pending':
                return <Warning className="text-yellow-500" />;
        }
    };

    const getStatusClass = (status: Order['status']) => {
        switch (status) {
            case 'delivered':
                return 'bg-green-100 text-green-800';
            case 'processing':
                return 'bg-blue-100 text-blue-800';
            case 'cancelled':
                return 'bg-red-100 text-red-800';
            case 'pending':
                return 'bg-yellow-100 text-yellow-800';
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold text-amazon-dark">Orders</h1>
                <div className="flex space-x-4">
                    <select className="bg-white border border-gray-300 rounded-md px-4 py-2 text-sm">
                        <option>All Orders</option>
                        <option>Delivered</option>
                        <option>Processing</option>
                        <option>Pending</option>
                        <option>Cancelled</option>
                    </select>
                    <input
                        type="text"
                        placeholder="Search orders..."
                        className="border border-gray-300 rounded-md px-4 py-2 text-sm"
                    />
                </div>
            </div>

            <div className="bg-white shadow-md rounded-lg overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Order ID
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Customer
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Date
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Items
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Total
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Status
                            </th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Actions
                            </th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {orders.map((order) => (
                            <tr key={order.id} className="hover:bg-gray-50">
                                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-amazon-dark">
                                    {order.id}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {order.customerName}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {order.date}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {order.items}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    ₹{order.total.toFixed(2)}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <div className="flex items-center">
                                        {getStatusIcon(order.status)}
                                        <span className={`ml-2 px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusClass(order.status)}`}>
                                            {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                                        </span>
                                    </div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    <button className="text-amazon-orange hover:text-amazon-orange-hover">
                                        View Details
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="flex justify-between items-center">
                <div className="text-sm text-gray-500">
                    Showing 1 to 4 of 4 orders
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

export default Orders; 