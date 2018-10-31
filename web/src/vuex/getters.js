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
                //  todo 可以更改错误的计算结果来测下单接口
                total += usefulCartList[i].PRnum * usefulCartList[i].PRprice;
            }
        }

        return total;
    },
    // 计算快递费
    payDeliverFee: state=>{
        let usefulCartList =  state.cartList.filter(cart => cart.PRnum != 0),
            fee = 0;

        if(usefulCartList.length > 1){

        }else if(usefulCartList.length == 1){
            fee = usefulCartList[0].PRlogisticsfee || 0;
        }

        return fee;
    },

}
