$(document).ready( function () {
    var hash = hashUrl();
    var sortBy = hash['sort'];
    if (sortBy == 'now_price') {
        $("#sortPriceButton").addClass("active");
    } else if (sortBy == 'merchant') {
        $("#sortMerchantButton").addClass("active");
    } else {
        $("#sortNameButton").addClass("active");
    }
});

function modify_Url_parameter(param, value) {
    var hash = hashUrl();
    var parser = document.createElement('a');
    parser.href = location.href;

    if (hash[param] == value) {
        // If value same, then change sort order
        if (hash['order'] == -1) {
            hash['order'] = 1;
        } else {
            hash['order'] = -1;
        }
    } else {
        // if value not same, then change value
        // and reset sort order to 1
        hash[param] = value;
        hash['order'] = 1;
    }

    // convert the hashmap back into param string
    var list = [];
    Object.keys(hash).forEach(function(key) {
        list.push(key + '=' + hash[key]);
    });
    parser.search = '?' + list.join('&');
    return parser.href;
}

function hashUrl() {
    var hash = {};
    var parser = document.createElement('a');
    parser.href = location.href;
    // split the request params
    var parameters = parser.search.split(/\?|&/);

    // convert params string into a hashmap
    for (var i = 0; i < parameters.length; i++) {
        if (!parameters[i])
            continue;
        var ary = parameters[i].split('=');
        hash[ary[0]] = ary[1];
    }
    return hash;
}