require('dotenv').config();
const axios = require('axios');

// Axios Client declaration
const api = axios.create({
  baseURL: 'http://127.0.0.1:5000',
  timeout: process.env.TIMEOUT || 5000,
});

// Generic GET request function
const post = async (url, headers, body) => {
  const response = await api.post(url, body, { headers: headers });
  const { status, data } = response;
  if (status == 201) {
    return data;
  }
  throw new Error(data);
};

module.exports = {
  createCustomer: (headers, body) => post(`/customers`, headers, body),
  createPaymentMethod: (headers, body) => post(`/payment_methods`, headers, body),
  createSale: (headers, body) => post(`/sales`, headers, body),
};
