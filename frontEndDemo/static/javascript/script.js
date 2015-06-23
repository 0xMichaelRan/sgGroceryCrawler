function URL_add_parameter(url, param, value) {
    var hash = {};
    var parser = document.createElement('a');
    parser.href = url;
    // split the request params
    var parameters = parser.search.split(/\?|&/);

    // convert params string into a hashmap
    for (var i = 0; i < parameters.length; i++) {
        if (!parameters[i])
            continue;
        var ary = parameters[i].split('=');
        hash[ary[0]] = ary[1];
    }

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