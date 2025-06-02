function parseShortNumber(str) {
    const num = parseFloat(str);
    if (str.toUpperCase().endsWith('K')) {
        return String(num * 1000);
    } else if (str.toUpperCase().endsWith('M')) {
        return String(num * 1000000);
    } else {
        return str;
    }
}