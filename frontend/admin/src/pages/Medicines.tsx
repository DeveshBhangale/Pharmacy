import React, { useState } from 'react';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';

interface Medicine {
    id: string;
    name: string;
    category: string;
    price: number;
    stock: number;
    manufacturer: string;
    image: string;
}

const Medicines: React.FC = () => {
    // TODO: Replace with actual API call
    const [medicines] = useState<Medicine[]>([
        {
            id: 'MED001',
            name: 'Paracetamol 500mg',
            category: 'Pain Relief',
            price: 49.99,
            stock: 500,
            manufacturer: 'HealthCare Pharma',
            image: 'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
        },
        {
            id: 'MED002',
            name: 'Vitamin D3 1000 IU',
            category: 'Supplements',
            price: 299.99,
            stock: 200,
            manufacturer: 'Wellness Labs',
            image: 'https://images.unsplash.com/photo-1577174881658-0f30ed549adc?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
        },
        {
            id: 'MED003',
            name: 'Blood Pressure Monitor',
            category: 'Medical Devices',
            price: 1999.99,
            stock: 50,
            manufacturer: 'MedTech Solutions',
            image: 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
        },
        {
            id: 'MED004',
            name: 'First Aid Kit',
            category: 'First Aid',
            price: 799.99,
            stock: 100,
            manufacturer: 'SafetyFirst Medical',
            image: 'https://images.unsplash.com/photo-1603398938378-e54eab446dde?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
        }
    ]);

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold text-amazon-dark">Medicines</h1>
                <div className="flex space-x-4">
                    <input
                        type="text"
                        placeholder="Search medicines..."
                        className="border border-gray-300 rounded-md px-4 py-2 text-sm"
                    />
                    <select className="bg-white border border-gray-300 rounded-md px-4 py-2 text-sm">
                        <option>All Categories</option>
                        <option>Pain Relief</option>
                        <option>Supplements</option>
                        <option>Medical Devices</option>
                        <option>First Aid</option>
                    </select>
                    <button className="bg-amazon-orange text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-amazon-orange-hover flex items-center">
                        <AddIcon className="w-5 h-5 mr-1" />
                        Add Medicine
                    </button>
                </div>
            </div>

            <div id="medicines-content" className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {medicines.map((medicine) => (
                    <div key={medicine.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                        <div className="h-48 overflow-hidden">
                            <img
                                src={medicine.image}
                                alt={medicine.name}
                                className="w-full h-full object-cover"
                            />
                        </div>
                        <div className="p-4">
                            <div className="flex justify-between items-start">
                                <div>
                                    <h3 className="text-lg font-semibold text-amazon-dark">{medicine.name}</h3>
                                    <p className="text-sm text-gray-500">{medicine.category}</p>
                                </div>
                                <div className="flex space-x-2">
                                    <button className="text-blue-500 hover:text-blue-700">
                                        <EditIcon className="w-5 h-5" />
                                    </button>
                                    <button className="text-red-500 hover:text-red-700">
                                        <DeleteIcon className="w-5 h-5" />
                                    </button>
                                </div>
                            </div>
                            <div className="mt-4">
                                <div className="flex justify-between items-center">
                                    <span className="text-lg font-bold text-amazon-orange">₹{medicine.price.toFixed(2)}</span>
                                    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${medicine.stock > 100
                                        ? 'bg-green-100 text-green-800'
                                        : medicine.stock > 20
                                            ? 'bg-yellow-100 text-yellow-800'
                                            : 'bg-red-100 text-red-800'
                                        }`}>
                                        Stock: {medicine.stock}
                                    </span>
                                </div>
                                <p className="text-sm text-gray-500 mt-2">Manufacturer: {medicine.manufacturer}</p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            <div className="flex justify-between items-center">
                <div className="text-sm text-gray-500">
                    Showing 1 to 4 of 4 medicines
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

export default Medicines; 