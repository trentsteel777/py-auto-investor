TODO:
    Create multiple strategies that run in the main for loop
    Get strike price calculator function right (increments should not always be 5)
    don't incorporate a portfolio amount / fum to work with
        just calculate profit/loss of each strategy over the period
    bring in multiple symbols
    bring in real data

https://www.interactivebrokers.ie/en/trading/margin-options.php

https://stackoverflow.com/questions/1237899/jquery-get-all-values-from-table-column
https://www.magicformulainvesting.com/Screening/StockScreening
var items=[], options=[];

//Iterate all td's in second column
$('.screeningdata tbody tr td:nth-child(2)').each( function(){
   //add item to array
   items.push( $(this).text() );       
});
console.log(items)