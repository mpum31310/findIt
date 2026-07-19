var app = angular.module('scanofinderApp', ['ngRoute']);

app.config(function($routeProvider, $httpProvider) {
    $routeProvider
        .when('/', {
            templateUrl: '/static/templates/home.html',
            controller: 'HomeController'
        })
        .when('/register', {
            templateUrl: '/static/templates/register.html',
            controller: 'AuthController'
        })
        .when('/login', {
            templateUrl: '/static/templates/login.html',
            controller: 'AuthController'
        })
        .when('/profile', {
            templateUrl: '/static/templates/profile.html',
            controller: 'ProfileController',
            resolve: {
                auth: function(AuthService) {
                    return AuthService.checkAuth();
                }
            }
        })
        .when('/children', {
            templateUrl: '/static/templates/children-list.html',
            controller: 'ChildrenListController',
            resolve: {
                auth: function(AuthService) {
                    return AuthService.checkAuth();
                }
            }
        })
        .when('/children/add', {
            templateUrl: '/static/templates/child-add.html',
            controller: 'ChildAddController',
            resolve: {
                auth: function(AuthService) {
                    return AuthService.checkAuth();
                }
            }
        })
        .when('/children/:id', {
            templateUrl: '/static/templates/child-detail.html',
            controller: 'ChildDetailController',
            resolve: {
                auth: function(AuthService) {
                    return AuthService.checkAuth();
                }
            }
        })
        .when('/items', {
            templateUrl: '/static/templates/items-list.html',
            controller: 'ItemsListController',
            resolve: {
                auth: function(AuthService) {
                    return AuthService.checkAuth();
                }
            }
        })
        .when('/items/add', {
            templateUrl: '/static/templates/item-add.html',
            controller: 'ItemAddController',
            resolve: {
                auth: function(AuthService) {
                    return AuthService.checkAuth();
                }
            }
        })
        .when('/items/:id', {
            templateUrl: '/static/templates/item-detail.html',
            controller: 'ItemDetailController',
            resolve: {
                auth: function(AuthService) {
                    return AuthService.checkAuth();
                }
            }
        })
        .when('/messages', {
            templateUrl: '/static/templates/messages.html',
            controller: 'MessagesController',
            resolve: {
                auth: function(AuthService) {
                    return AuthService.checkAuth();
                }
            }
        })
        .when('/subscription', {
            templateUrl: '/static/templates/subscription.html',
            controller: 'SubscriptionController',
            resolve: {
                auth: function(AuthService) {
                    return AuthService.checkAuth();
                }
            }
        })
        .when('/scan/:qrData', {
            templateUrl: '/static/templates/scan.html',
            controller: 'ScanController'
        })
        .when('/about', {
            templateUrl: '/static/templates/about.html',
            controller: 'AboutController'
        })
        .when('/terms', {
            templateUrl: '/static/templates/terms.html',
            controller: 'TermsController'
        })
        .when('/privacy', {
            templateUrl: '/static/templates/privacy.html',
            controller: 'PrivacyController'
        })
        .otherwise({
            redirectTo: '/'
        });
    
    // Add JWT token to all requests
    $httpProvider.interceptors.push(function($q, $location, AuthService) {
        return {
            request: function(config) {
                var token = AuthService.getToken();
                if (token) {
                    config.headers.Authorization = 'Bearer ' + token;
                }
                return config;
            },
            responseError: function(response) {
                if (response.status === 401) {
                    AuthService.logout();
                    $location.path('/login');
                }
                if (response.status === 403 && response.data.subscription_required) {
                    $location.path('/subscription');
                }
                return $q.reject(response);
            }
        };
    });
});

app.run(function($rootScope, AuthService) {
    $rootScope.$on('$routeChangeStart', function(event, next, current) {
        if (next.resolve && next.resolve.auth) {
            if (!AuthService.isAuthenticated()) {
                event.preventDefault();
                $rootScope.$evalAsync(function() {
                    window.location.href = '/#/login';
                });
            }
        }
    });
    
    // Check authentication on app load
    AuthService.checkAuth();
});

