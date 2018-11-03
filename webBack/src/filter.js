/**
 * Created by syen on 2017/7/26.
 */
export default function (Vue) {
    //数字转化
  Vue.filter('hanhua',function (num) {
        switch (num){
          case 1:return '星期一';
          case 2:return '星期二';
          case 3:return '星期三';
          case 4:return '星期四';
          case 5:return '星期五';
          case 6:return '星期六';
          case 0:return '星期日';
        }
  });
  //周转化
  Vue.filter('weekChange',function (num) {
    num = Number(num);
    switch (num){
      case 1:return '周一';
      case 2:return '周二';
      case 3:return '周三';
      case 4:return '周四';
      case 5:return '周五';
      case 6:return '周六';
      case 0:return '周日';
    }
  });
  Vue.filter('percent',function (num) {
     return `${num}%`
  })
  Vue.filter('ToFixed2',function (num) {
      if(!!num){
        return Number(num).toFixed(2);
      }else {
        return num;
      }
  })
  Vue.filter('line',function (str) {
    return str.replace('-','/').replace('-','/')
  })
  Vue.filter('TransferNum',function (str) {
     if(str==null){
       return ''
     }else{
       return Number(str)
     }
  })
}
