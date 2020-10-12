require('dotenv').config(); // read .env files
const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = process.env.PORT || 3000;

const { createCustomer, createPaymentMethod, createSale } = require('./lib/primer-service');

// Set public folder as root
app.use(express.static('public'));

// Express Error handler
const errorHandler = (err, req, res) => {
  if (err.response) {
    // The request was made and the server responded with a status code
    // that falls out of the range of 2xx
    res.status(403).send({ title: 'Server responded with an error', message: err.message });
  } else if (err.request) {
    // The request was made but no response was received
    res.status(503).send({ title: 'Unable to communicate with server', message: err.message });
  } else {
    // Something happened in setting up the request that triggered an Error
    res.status(500).send({ title: 'An unexpected error occurred', message: err.message });
  }
};

// Parse POST data as URL encoded data
app.use(bodyParser.urlencoded({
  extended: true,
}));

// Parse POST data as JSON
app.use(bodyParser.json());

app.post('/customer', async (req, res) => {
  try {
    const body  = req.body;
    const headers = { 'Content-Type': 'application/json' }
    const data = await createCustomer(headers, body);
    res.setHeader('Content-Type', 'application/json');
    res.send(data);

  } catch (error) {
    errorHandler(error, req, res);
  }
});

app.post('/payment-method', async (req, res) => {
  try {
    const body  = req.body;
    const headers = req.headers;
    const data = await createPaymentMethod(headers, body);
    res.setHeader('Content-Type', 'application/json');
    res.send(data);

  } catch (error) {
    errorHandler(error, req, res);
  }
});

app.post('/sale', async (req, res) => {
  try {
    const body  = req.body;
    const headers = req.headers;
    const data = await createSale(headers, body);
    res.setHeader('Content-Type', 'application/json');
    res.send(data);

  } catch (error) {
    errorHandler(error, req, res);
  }
});

// Allow front-end access to node_modules folder
app.use('/scripts', express.static(`${__dirname}/node_modules/`));

// Redirect all traffic to index.html
app.use((req, res) => res.sendFile(`${__dirname}/public/index.html`));

// Listen for HTTP requests on port 3000
app.listen(port, () => {
  console.log('listening on %d', port);
});
