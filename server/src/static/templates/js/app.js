        var myApp = angular.module('myApp',[]).config(function($interpolateProvider) {
            $interpolateProvider.startSymbol('[[');
            $interpolateProvider.endSymbol(']]');
        });


        myApp.factory('ApiRequest', ['$rootScope', '$http', '$log', '$q', function ($rootScope,
        $http, $log, $q) {
    var ApiRequest = {};
    var apiData = {}
    ApiRequest.sendRequest = function (data) {
        try {
            return $http({
                method: data.requestType,
                url: data.requestUrl,
                headers: data.headers,
                data: data.requestData
            });
        }
        catch (e) {
            $log.error('ApiRequest Factory.ApiRequest.sendRequest  - ' + e.message);
            return false;
        }
    };
    ApiRequest.getProjectData = function (data) {
        try {
            if (apiData[parseInt(data.projectId, 10)]) {
                deferred = $q.defer();
                deferred.resolve(apiData[parseInt(data.projectId, 10)]);
                return deferred.promise;
            }
            else {
                return $http({
                    method: data.requestType,
                    url: data.requestUrl,
                    headers: data.headers,
                    data: data.requestData
                }).then(function(result) {
//                    Logger({level:'debug', log_message: MessageGenerator({type:'success', module:['api', 'manage','project','list']}), log_object: result})
                    apiData[parseInt(data.projectId, 10)] = result;
                    return result;
                });
            }
        }
        catch (e) {
            $log.error('ApiRequest Factory.ApiRequest.getProjectData  - ' + e.message);
            return false;
        }
    };
    ApiRequest.resetProjectData = function (projectId, updatedData) {
        apiData[parseInt(projectId, 10)] = updatedData
    };
    return ApiRequest;
}]);
        myApp.controller('Logincontroller', ['$scope', 'ApiRequest', function($scope, ApiRequest) {
            $scope.contacts = ["hi@email.com", "hello@email.com", {'name': 'sumit'}];
            $scope.name1 = 'sumit';
            $scope.bool = false;
            console.log($scope.name1);
            $scope.add = function() {
                $scope.contacts.push($scope.contact);
                $scope.contact = "";
            }
            $scope.login = function(email, pword) {
                console.log("loogging in ", email, pword);
                var form_obj = new FormData();
                form_obj.append(email, pword);

                ApiRequest.sendRequest({
                    requestType: 'POST',
                    requestUrl: '/api/v1/auth/login/',
                    requestData: {
                        email: email,
                        password: pword
                    }
                }).then(function (result){
                    console.log("data sent", result);
                })
            }
        }]);