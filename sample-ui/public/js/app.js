window.addEventListener('load', () => {
  const el = $('#app');

  // Compile Handlebar Templates
  const errorTemplate = Handlebars.compile($('#error-template').html());
  const customerTemplate = Handlebars.compile($('#customer-template').html());
  const paymentMethodTemplate = Handlebars.compile($('#payment-method-template').html());
  const saleTemplate = Handlebars.compile($('#sale-template').html());

  // Router Declaration
  const router = new Router({
    mode: 'history',
    page404: (path) => {
      const html = errorTemplate({
        color: 'yellow',
        title: 'Error 404 - Page NOT Found!',
        message: `The path '/${path}' does not exist on this site`,
      });
      el.html(html);
    },
  });

  // Instantiate api handler
  const api = axios.create({
    baseURL: 'http://localhost:3000',
    timeout: 5000,
  });

  const showError = (error) => {
    const { title, message } = error.response.data;
    const html = errorTemplate({ color: 'red', title, message });
    el.html(html);
  };


  const createCustomer = async () => {
    // Extract form data
    const first_name = $('#first_name').val();
    const last_name = $('#last_name').val();
    const email = $('#email').val();
    const company = $('#company').val();
    const phone = $('#phone').val();
    // Send post data to Express(proxy) server
    const data = {
      first_name,
      last_name,
      email,
      company,
      phone
    }
    try {
      const response = await api.post('/customer', data);
      const { token } = response.data
      $('#customer-token').html(`token ${token}`);
    } catch (error) {
      showError(error);
    } finally {
      $('#result-segment-customer').removeClass('loading');
    }
  };

  const createCustomerHandler = () => {
    if ($('.ui.form').form('is valid')) {
      // hide error message
      $('.ui.error.message').hide();
      // Post to Express server
      $('#result-segment-customer').addClass('loading');
      createCustomer();
      // Prevent page from submitting to server
      return false;
    }
    return true;
  };

  const createPaymentMethod = async () => {
    // Extract form data
    const customer_token = $('#customer_token').val();
    const cardholder_name = $('#cardholder_name').val();
    const number = $('#number').val();
    const cvv = $('#cvv').val();
    const expiration_date = $('#expiration_date').val();
    // Send post data to Express(proxy) server
    const data = {
      cardholder_name,
      number,
      cvv,
      expiration_date
    }

    const headers = {
      'Authorization': `Bearer ${customer_token}`
    }

    try {
      const response = await api.post('/payment-method', data, { headers: headers });
      const { token } = response.data
      $('#payment-method-token').html(`token ${token}`);
    } catch (error) {
      showError(error);
    } finally {
      $('#result-segment-payment').removeClass('loading');
    }
  };

  const createPaymentMethodHandler = () => {
    if ($('.ui.form').form('is valid')) {
      // hide error message
      $('.ui.error.message').hide();
      // Post to Express server
      $('#result-segment-payment').addClass('loading');
      createPaymentMethod();
      // Prevent page from submitting to server
      return false;
    }
    return true;
  };

  const createSale = async () => {
    // Extract form data
    const customer_token = $('#customer_sale_token').val();
    const payment_method_token = $('#payment_method_token').val();
    const amount = $('#amount').val();
    // Send post data to Express(proxy) server
    const data = {
      amount
    }

    const headers = {
      'Authorization': `Bearer ${customer_token}`,
      'x-pay-token': `${payment_method_token}`
    }

    try {
      const response = await api.post('/sale', data, { headers: headers });
      const { message } = response.data
      $('#sale-message').html(`${message}`);
    } catch (error) {
      showError(error);
    } finally {
      $('#result-segment-sale').removeClass('loading');
    }
  };

  const createSaleHandler = () => {
    if ($('.ui.form').form('is valid')) {
      // hide error message
      $('.ui.error.message').hide();
      // Post to Express server
      $('#result-segment-sale').addClass('loading');
      createSale();
      // Prevent page from submitting to server
      return false;
    }
    return true;
  };

  router.add('/', () => {
    let html = customerTemplate();
    el.html(html);
    $('.loading').removeClass('loading');
    // Validate Form Inputs
    $('.ui.form.customer').form({
      fields: {
        first_name: 'empty',
        last_name: 'empty',
        email: 'empty'
      },
    });
    $('#customer-button').click(createCustomerHandler);
  });

  router.add('/payment-method', () => {
    let html = paymentMethodTemplate();
    el.html(html);
    $('.loading').removeClass('loading');
    // Validate Form Inputs
    $('.ui.form.payment').form({
      fields: {
        customer_token: 'empty',
        cardholder_name: 'empty',
        number: 'empty',
        cvv: 'empty',
        expiration_date: 'empty'
      },
    });
    $('#payment-button').click(createPaymentMethodHandler);
  });

  router.add('/sale', () => {
    let html = saleTemplate();
    el.html(html);
    $('.loading').removeClass('loading');
    // Validate Form Inputs
    $('.ui.form.sale').form({
      fields: {
        customer_sale_token: 'empty',
        payment_method_token: 'empty',
        amount: 'empty'
      },
    });
    $('#sale-button').click(createSaleHandler);
  });

  // Navigate app to current url
  router.navigateTo(window.location.pathname);

  // Highlight Active Menu on Refresh/Page Reload
  const link = $(`a[href$='${window.location.pathname}']`);
  link.addClass('active');

  $('a').on('click', (event) => {
    // Block browser page load
    event.preventDefault();

    // Highlight Active Menu on Click
    const target = $(event.target);
    $('.item').removeClass('active');
    target.addClass('active');

    // Navigate to clicked url
    const href = target.attr('href');
    const path = href.substr(href.lastIndexOf('/'));
    router.navigateTo(path);
  });
});

