// https://stockanalysis.com/list/sp-500-stocks/

// https://github.com/bfaure/StockSpider/blob/master/iShares-Russell-3000-ETF_fund.csv
var s = document.getElementsByClassName('sym')
var a = []
for(var i = 1; i < s.length; i++) {
    a.push(s[i].innerText)
}
a = a.sort()
var r = ""
for(var i = 0; i < a.length; i++) {
    r+= "'" +a[i]+ "', "
}
console.log(r)