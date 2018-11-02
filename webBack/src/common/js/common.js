/**
 * Created by syen on 2017/7/26.
 */
const common = {
  //获取当前周
  getWeek: function () {
    var time, week, checkDate = new Date(new Date());
    checkDate.setDate(checkDate.getDate() + 4 - (checkDate.getDay() || 7));
    time = checkDate.getTime();
    checkDate.setMonth(0);
    checkDate.setDate(1);
    week = Math.floor(Math.round((time - checkDate) / 86400000) / 7) + 1;
    return week;
  },
  //深度克隆
  deepClone: function (obj) {
    var str, newobj = obj.constructor === Array ? [] : {};
    if (typeof obj !== 'object') {
      return;
    } else if (typeof window !== 'undefined' && window.JSON) {
      str = JSON.stringify(obj), //系列化对象
        newobj = JSON.parse(str); //还原
    } else {
      for (var i in obj) {
        newobj[i] = typeof obj[i] === 'object' ?
          deepClone(obj[i]) : obj[i];
      }
    }
    return newobj;
  },
  //去重
  removeRepeat: function (obj, cbj) {
    obj = this.deepClone(obj);
    cbj = this.deepClone(cbj);
    let obj1 = JSON.stringify(obj);
    let cbj1 = JSON.stringify(cbj);
    if (obj1.indexOf(cbj1) < 0) {
      obj.push(cbj)
    }
    return obj
  },
  formmatDate: function (date) {
    var arr = [];
    arr[0] = date.getFullYear();
    arr[1] = date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1;
    arr[2] = date.getDate() < 10 ? '0' + date.getDate() : date.getDate();
    return `${arr[0]}-${arr[1]}-${arr[2]}`
  },
  //json数组排序
  sortArr:function sortByKey(array, key,type) {
    return array.sort(function(a, b) {
      var x = a[key]; var y = b[key];
      if(type=='big'){
        return ((x < y) ? -1 : ((x > y) ? 1 : 0));
      }else{
        return ((x > y) ? -1 : ((x < y) ? 1 : 0));
      }

    });
  }
}
export default common
