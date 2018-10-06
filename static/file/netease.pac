function FindProxyForURL(url, host) {
    if (host == "music.163.com" || host == "ip.ws.126.net") {
        return "PROXY 79.137.38.20:80";
    } else if (host == "music.httpdns.c.163.com") {
        return "PROXY 127.0.0.1:9999";
    } else if (host == "m10.music.126.net") {
        return "PROXY 125.39.1.27:80";
    }
    return "DIRECT";
}