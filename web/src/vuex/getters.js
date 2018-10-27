export default {
    // 删选出PRnum不为0的
    usefulCartList: state=>{
        return state.cartList.filter(cart => cart.PRnum != 0);
    },
    // 计算总价
    cartTotalPrice: state=>{
        let usefulCartList =  state.cartList.filter(cart => cart.PRnum != 0),
            total = 0;

        if(usefulCartList){
            for (let i = 0; i < usefulCartList.length; i++) {
                total += usefulCartList[0].PRnum * usefulCartList[0].PRprice;
            }
        }

        return total;
    },
    // 计算快递费
    payDeliverFee: state=>{
        let usefulCartList =  state.cartList.filter(cart => cart.PRnum != 0),
            fee = 0;

        if(usefulCartList.length > 1){

        }else{
            fee = usefulCartList[0].PRlogisticsfee || 0;
        }

        return fee;
    },

}
