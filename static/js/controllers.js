app.controller('HomeController', function($scope, $location) {
    $scope.goToRegister = function() {
        $location.path('/register');
    };
    
    $scope.goToLogin = function() {
        $location.path('/login');
    };
});

app.controller('AuthController', function($scope, $location, AuthService) {
    $scope.isLogin = $location.path() === '/login';
    $scope.loading = false;
    $scope.error = '';
    
    $scope.user = {
        username: '',
        email: '',
        cell_number: '',
        password: '',
        password2: ''
    };
    
    $scope.submit = function() {
        $scope.loading = true;
        $scope.error = '';
        
        if ($scope.isLogin) {
            AuthService.login({
                username: $scope.user.username,
                password: $scope.user.password
            }).then(function() {
                $location.path('/profile');
            }).catch(function(error) {
                $scope.error = error.data?.error || 'Login failed';
                $scope.loading = false;
            });
        } else {
            if ($scope.user.password !== $scope.user.password2) {
                $scope.error = 'Passwords do not match';
                $scope.loading = false;
                return;
            }
            
            AuthService.register({
                username: $scope.user.username,
                email: $scope.user.email,
                cell_number: $scope.user.cell_number,
                password: $scope.user.password,
                password2: $scope.user.password2
            }).then(function() {
                $location.path('/profile');
            }).catch(function(error) {
                $scope.error = error.data?.error || 'Registration failed';
                $scope.loading = false;
            });
        }
    };
});

app.controller('ProfileController', function($scope, AuthService, $http) {
    $scope.loading = true;
    $scope.user = AuthService.getUser();
    $scope.editing = false;
    $scope.success = '';
    $scope.error = '';
    
    $http.get('/api/auth/profile/').then(function(response) {
        $scope.user = response.data;
        $scope.loading = false;
    });
    
    $scope.edit = function() {
        $scope.editing = true;
        $scope.editUser = angular.copy($scope.user);
    };
    
    $scope.save = function() {
        $scope.loading = true;
        $http.put('/api/auth/profile/update/', $scope.editUser).then(function(response) {
            $scope.user = response.data;
            AuthService.setUser(response.data);
            $scope.editing = false;
            $scope.success = 'Profile updated successfully';
            $scope.loading = false;
        }).catch(function(error) {
            $scope.error = 'Failed to update profile';
            $scope.loading = false;
        });
    };
    
    $scope.cancel = function() {
        $scope.editing = false;
    };
});

app.controller('ChildrenListController', function($scope, ChildrenService, $location) {
    $scope.loading = true;
    $scope.children = [];
    
    $scope.loadChildren = function() {
        ChildrenService.list().then(function(response) {
            $scope.children = response.data.results || response.data;
            $scope.loading = false;
        });
    };
    
    $scope.addChild = function() {
        $location.path('/children/add');
    };
    
    $scope.viewChild = function(id) {
        $location.path('/children/' + id);
    };
    
    $scope.loadChildren();
});

app.controller('ChildAddController', function($scope, ChildrenService, $location) {
    $scope.loading = false;
    $scope.error = '';
    $scope.success = '';
    
    $scope.child = {
        name: '',
        surname: '',
        grade: '',
        school: ''
    };
    
    $scope.submit = function() {
        $scope.loading = true;
        $scope.error = '';
        
        ChildrenService.create($scope.child).then(function() {
            $scope.success = 'Child added successfully';
            setTimeout(function() {
                $location.path('/children');
            }, 1000);
        }).catch(function(error) {
            $scope.error = error.data?.error || 'Failed to add child';
            $scope.loading = false;
        });
    };
});

app.controller('ChildDetailController', function($scope, $routeParams, ChildrenService, $location) {
    $scope.loading = true;
    $scope.editing = false;
    $scope.error = '';
    $scope.success = '';
    
    $scope.loadChild = function() {
        ChildrenService.get($routeParams.id).then(function(response) {
            $scope.child = response.data;
            $scope.editChild = angular.copy($scope.child);
            $scope.loading = false;
        });
    };
    
    $scope.edit = function() {
        $scope.editing = true;
    };
    
    $scope.save = function() {
        $scope.loading = true;
        ChildrenService.update($routeParams.id, $scope.editChild).then(function(response) {
            $scope.child = response.data;
            $scope.editing = false;
            $scope.success = 'Child updated successfully';
            $scope.loading = false;
        }).catch(function(error) {
            $scope.error = 'Failed to update child';
            $scope.loading = false;
        });
    };
    
    $scope.delete = function() {
        if (confirm('Are you sure you want to delete this child?')) {
            $scope.loading = true;
            ChildrenService.delete($routeParams.id).then(function() {
                $location.path('/children');
            });
        }
    };
    
    $scope.cancel = function() {
        $scope.editing = false;
        $scope.editChild = angular.copy($scope.child);
    };
    
    $scope.loadChild();
});

app.controller('ItemsListController', function($scope, ItemsService, ChildrenService, $location) {
    $scope.loading = true;
    $scope.items = [];
    $scope.children = [];
    
    $scope.loadItems = function() {
        ItemsService.list().then(function(response) {
            $scope.items = response.data.results || response.data;
            $scope.loading = false;
        });
    };
    
    $scope.loadChildren = function() {
        ChildrenService.list().then(function(response) {
            $scope.children = response.data.results || response.data;
        });
    };
    
    $scope.addItem = function() {
        $location.path('/items/add');
    };
    
    $scope.viewItem = function(id) {
        $location.path('/items/' + id);
    };
    
    $scope.getChildName = function(item) {
        if (item.child) {
            return item.child.name + ' ' + item.child.surname;
        }
        return 'Unassigned';
    };
    
    $scope.loadItems();
    $scope.loadChildren();
});

app.controller('ItemAddController', function($scope, ItemsService, ChildrenService, $location) {
    $scope.loading = false;
    $scope.error = '';
    $scope.success = '';
    $scope.children = [];
    
    $scope.item = {
        name: '',
        description: '',
        child_id: null,
        item_image: null
    };
    
    $scope.loadChildren = function() {
        ChildrenService.list().then(function(response) {
            $scope.children = response.data.results || response.data;
        });
    };
    
    $scope.onFileSelect = function(files) {
        if (files && files.length > 0) {
            $scope.item.item_image = files[0];
        }
    };
    
    $scope.submit = function() {
        $scope.loading = true;
        $scope.error = '';
        
        ItemsService.create($scope.item).then(function(response) {
            $scope.success = 'Item added and QR code generated successfully';
            setTimeout(function() {
                $location.path('/items/' + response.data.id);
            }, 1500);
        }).catch(function(error) {
            $scope.error = error.data?.error || 'Failed to add item';
            $scope.loading = false;
        });
    };
    
    $scope.loadChildren();
});

app.controller('ItemDetailController', function($scope, $routeParams, ItemsService, ChildrenService, $location) {
    $scope.loading = true;
    $scope.editing = false;
    $scope.error = '';
    $scope.success = '';
    $scope.children = [];
    
    $scope.loadItem = function() {
        ItemsService.get($routeParams.id).then(function(response) {
            $scope.item = response.data;
            $scope.editItem = angular.copy($scope.item);
            $scope.loading = false;
        });
    };
    
    $scope.loadChildren = function() {
        ChildrenService.list().then(function(response) {
            $scope.children = response.data.results || response.data;
        });
    };
    
    $scope.edit = function() {
        $scope.editing = true;
    };
    
    $scope.onFileSelect = function(files) {
        if (files && files.length > 0) {
            $scope.editItem.item_image = files[0];
        }
    };
    
    $scope.save = function() {
        $scope.loading = true;
        ItemsService.update($routeParams.id, $scope.editItem).then(function(response) {
            $scope.item = response.data;
            $scope.editing = false;
            $scope.success = 'Item updated successfully';
            $scope.loading = false;
        }).catch(function(error) {
            $scope.error = 'Failed to update item';
            $scope.loading = false;
        });
    };
    
    $scope.delete = function() {
        if (confirm('Are you sure you want to delete this item?')) {
            $scope.loading = true;
            ItemsService.delete($routeParams.id).then(function() {
                $location.path('/items');
            });
        }
    };
    
    $scope.downloadQR = function() {
        if ($scope.item.qr_code_url) {
            window.open($scope.item.qr_code_url, '_blank');
        }
    };
    
    $scope.cancel = function() {
        $scope.editing = false;
        $scope.loadItem();
    };
    
    $scope.loadItem();
    $scope.loadChildren();
});

app.controller('MessagesController', function($scope, MessagesService) {
    $scope.loading = true;
    $scope.messages = [];
    
    $scope.loadMessages = function() {
        MessagesService.list().then(function(response) {
            $scope.messages = response.data.results || response.data;
            $scope.loading = false;
        });
    };
    
    $scope.markRead = function(message) {
        if (!message.is_read) {
            MessagesService.markRead(message.id).then(function() {
                message.is_read = true;
            });
        }
    };
    
    $scope.loadMessages();
});

app.controller('ScanController', function($scope, $routeParams, ItemsService, MessagesService) {
    $scope.loading = true;
    $scope.item = null;
    $scope.error = '';
    $scope.messageSent = false;
    
    $scope.message = {
        sender_name: '',
        sender_email: '',
        sender_phone: '',
        message: '',
        item_qr_data: $routeParams.qrData
    };
    
    $scope.loadItem = function() {
        ItemsService.getByQR($routeParams.qrData).then(function(response) {
            $scope.item = response.data;
            $scope.loading = false;
        }).catch(function(error) {
            $scope.error = 'Item not found';
            $scope.loading = false;
        });
    };
    
    $scope.sendMessage = function() {
        $scope.loading = true;
        MessagesService.create($scope.message).then(function() {
            $scope.messageSent = true;
            $scope.loading = false;
        }).catch(function(error) {
            $scope.error = 'Failed to send message';
            $scope.loading = false;
        });
    };
    
    $scope.loadItem();
});

app.controller('SubscriptionController', function($scope, PaymentService, AuthService, $http) {
    $scope.loading = false;
    $scope.subscription = null;
    $scope.error = '';
    $scope.success = '';
    $scope.stripe = null;
    $scope.cardElement = null;
    
    $scope.loadSubscription = function() {
        PaymentService.getSubscription().then(function(response) {
            $scope.subscription = response.data;
        });
    };
    
    $scope.initStripe = function() {
        if (typeof Stripe !== 'undefined') {
            $http.get('/api/payments/stripe-key/').then(function(response) {
                var publishableKey = response.data.publishable_key;
                if (publishableKey) {
                    $scope.stripe = Stripe(publishableKey);
                    var elements = $scope.stripe.elements();
                    $scope.cardElement = elements.create('card');
                    $scope.cardElement.mount('#card-element');
                } else {
                    $scope.error = 'Stripe is not configured. Please contact support.';
                }
            }).catch(function() {
                $scope.error = 'Failed to load payment configuration.';
            });
        }
    };
    
    $scope.subscribe = function() {
        if (!$scope.stripe || !$scope.cardElement) {
            $scope.error = 'Payment system not initialized. Please refresh the page.';
            return;
        }
        
        $scope.loading = true;
        $scope.error = '';
        
        PaymentService.createPaymentIntent().then(function(response) {
            $scope.stripe.confirmCardPayment(response.data.client_secret, {
                payment_method: {
                    card: $scope.cardElement
                }
            }).then(function(result) {
                if (result.error) {
                    $scope.error = result.error.message;
                    $scope.loading = false;
                } else {
                    PaymentService.confirmPayment(response.data.payment_id).then(function() {
                        $scope.success = 'Subscription activated successfully!';
                        $scope.loadSubscription();
                        $scope.loading = false;
                    }).catch(function(error) {
                        $scope.error = 'Payment processed but subscription activation failed. Please contact support.';
                        $scope.loading = false;
                    });
                }
            });
        }).catch(function(error) {
            $scope.error = error.data?.error || 'Failed to process payment';
            $scope.loading = false;
        });
    };
    
    $scope.loadSubscription();
    $scope.initStripe();
});

app.controller('AboutController', function($scope) {
    // Static content controller
});

app.controller('TermsController', function($scope) {
    // Static content controller
});

app.controller('PrivacyController', function($scope) {
    // Static content controller
});

// Navigation Controller
app.controller('NavController', function($scope, $location, AuthService) {
    $scope.isAuthenticated = function() {
        return AuthService.isAuthenticated();
    };
    
    $scope.getUser = function() {
        return AuthService.getUser();
    };
    
    $scope.logout = function() {
        AuthService.logout();
        $location.path('/');
    };
    
    $scope.isActive = function(path) {
        return $location.path() === path;
    };
});

