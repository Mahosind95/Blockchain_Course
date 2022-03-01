// SPDX-License-Identifier: GPL-3.0
//AdhiPaisa ICO

//Version of Compiler
pragma solidity >=0.7.0 <0.9.0;

contract adhipaisa_ico {
    // public variable can be accessed outside the contract, whereas privtae can be accessed only inside the 
    //contract

    //Introducing the total number of adhiPaisa available for sale
    uint public max_adhipaisa = 1000000;

    // Introducing the INR to adhiPaisa conversion rate
    uint public int_to_adhip = 100;

    //Inroducing total number of adhiPaisa that have been bought by Investor
    uint public total_hadcoins_bought = 0;

    //Mapping from the investor address to its equity in adhiPaisa and INR
    mapping(address => uint) equity_adhipaisa;
    mapping(address => uint) equity_inr;

    //Check if investor can buy coins. modifer is like a function
    modifier can_buy_adhipaisa(uint inr_invested){
        require (inr_invested * int_to_adhip + total_hadcoins_bought <= max_adhipaisa);
        _; // the function linked to modifier will only be applied if 
    }


    //Function Getting the equity in AdhiPaisa of an Investor
    //decribes address as an external entity
    function equity_in_adhipaisa(address investor)external returns (uint){
        return equity_adhipaisa[investor];
    }

    //Function Getting the equity in INR of an Investor
        function equity_in_inr(address investor)external returns (uint){
        return equity_inr[investor];
    }

    //Buying adhipaisa
    function buy_adhipaisa(address investor, uint inr_invested)external
    can_buy_adhipaisa(inr_invested){

        uint adhip_bought = inr_invested * int_to_adhip;
        equity_adhipaisa[investor] += adhip_bought;
        equity_inr[investor] = equity_adhipaisa[investor]/100;
        total_hadcoins_bought +=  adhip_bought;

    }

//Selling adhicoins
    function sell_adhipaisa(address investor, uint adhip_sold)external{

        equity_adhipaisa[investor] -= adhip_sold;
        equity_inr[investor] = equity_adhipaisa[investor]/100;
        total_hadcoins_bought -=  adhip_sold;
    }
}