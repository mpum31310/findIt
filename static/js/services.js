app.service('AuthService', function($http, $window, $q) {
    var self = this;
    
    this.getToken = function() {
        return $window.localStorage.getItem('access_token');
    };
    
    this.setToken = function(token) {
        $window.localStorage.setItem('access_token', token);
    };
    
    this.getRefreshToken = function() {
        return $window.localStorage.getItem('refresh_token');
    };
    
    this.setRefreshToken = function(token) {
        $window.localStorage.setItem('refresh_token', token);
    };
    
    this.getUser = function() {
        var userStr = $window.localStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    };
    
    this.setUser = function(user) {
        $window.localStorage.setItem('user', JSON.stringify(user));
    };
    
    this.isAuthenticated = function() {
        return !!this.getToken();
    };
    
    this.login = function(credentials) {
        return $http.post('/api/auth/login/', credentials).then(function(response) {
            self.setToken(response.data.access);
            self.setRefreshToken(response.data.refresh);
            self.setUser(response.data.user);
            return response.data;
        });
    };
    
    this.register = function(userData) {
        return $http.post('/api/auth/register/', userData).then(function(response) {
            self.setToken(response.data.access);
            self.setRefreshToken(response.data.refresh);
            self.setUser(response.data.user);
            return response.data;
        });
    };
    
    this.logout = function() {
        $window.localStorage.removeItem('access_token');
        $window.localStorage.removeItem('refresh_token');
        $window.localStorage.removeItem('user');
    };
    
    this.checkAuth = function() {
        if (this.isAuthenticated()) {
            return $q.resolve();
        }
        return $q.reject('Not authenticated');
    };
});

app.service('ChildrenService', function($http) {
    this.list = function() {
        return $http.get('/api/children/');
    };
    
    this.get = function(id) {
        return $http.get('/api/children/' + id + '/');
    };
    
    this.create = function(child) {
        return $http.post('/api/children/', child);
    };
    
    this.update = function(id, child) {
        return $http.put('/api/children/' + id + '/', child);
    };
    
    this.delete = function(id) {
        return $http.delete('/api/children/' + id + '/');
    };
});

app.service('ItemsService', function($http) {
    this.list = function() {
        return $http.get('/api/items/');
    };
    
    this.get = function(id) {
        return $http.get('/api/items/' + id + '/');
    };
    
    this.getByQR = function(qrData) {
        return $http.get('/api/items/qr/' + qrData + '/');
    };
    
    this.create = function(item) {
        var formData = new FormData();
        formData.append('name', item.name);
        formData.append('description', item.description || '');
        if (item.child_id) {
            formData.append('child_id', item.child_id);
        }
        if (item.item_image) {
            formData.append('item_image', item.item_image);
        }
        
        return $http.post('/api/items/', formData, {
            headers: {
                'Content-Type': undefined
            },
            transformRequest: angular.identity
        });
    };
    
    this.update = function(id, item) {
        var formData = new FormData();
        formData.append('name', item.name);
        formData.append('description', item.description || '');
        if (item.child_id) {
            formData.append('child_id', item.child_id);
        }
        if (item.item_image) {
            formData.append('item_image', item.item_image);
        }
        
        return $http.put('/api/items/' + id + '/', formData, {
            headers: {
                'Content-Type': undefined
            },
            transformRequest: angular.identity
        });
    };
    
    this.delete = function(id) {
        return $http.delete('/api/items/' + id + '/');
    };
});

app.service('MessagesService', function($http) {
    this.list = function() {
        return $http.get('/api/messages/');
    };
    
    this.get = function(id) {
        return $http.get('/api/messages/' + id + '/');
    };
    
    this.create = function(message) {
        return $http.post('/api/messages/create/', message);
    };
    
    this.markRead = function(id) {
        return $http.put('/api/messages/' + id + '/', {is_read: true});
    };
});

app.service('PaymentService', function($http) {
    this.getSubscription = function() {
        return $http.get('/api/payments/subscription/');
    };
    
    this.createPaymentIntent = function() {
        return $http.post('/api/payments/create-intent/');
    };
    
    this.confirmPayment = function(paymentId) {
        return $http.post('/api/payments/confirm/', {payment_id: paymentId});
    };
    
    this.getPaymentHistory = function() {
        return $http.get('/api/payments/history/');
    };
});

