import Vue from 'vue'
import 'echarts'
import http from 'axios'
import App from './App.vue'
Vue.config.productionTip = false
import store from './store/index';
import { Container, Header,Aside,Main,Dropdown,DropdownMenu,DropdownItem,Row,Col,Button,Select,Option,Upload,Dialog,Tooltip,Image,Input,FormItem,Form,Checkbox,Message,Table,TableColumn,Radio,RadioGroup,Loading} from 'element-ui';
import CollapseTransition from 'element-ui/lib/transitions/collapse-transition';
import VueTour from 'vue-tour'
import router from './routers'
Vue.prototype.$message=Message
require('vue-tour/dist/vue-tour.css')
Vue.prototype.$tours=VueTour
Vue.use(VueTour)
Vue.prototype.$http=http
Vue.use(Loading);
Vue.use(Container);
Vue.use(Header);
Vue.use(Aside);
Vue.use(Main);
Vue.use(DropdownMenu);
Vue.use(DropdownItem);
Vue.use(Row);
Vue.use(Col);
Vue.use(Dropdown);
Vue.use(Button);
Vue.use(Select);
Vue.use(Option);
Vue.use(Upload);
Vue.use(Dialog);
Vue.use(Tooltip);
Vue.use(Image);
Vue.use(Input);
Vue.use(FormItem);
Vue.use(Form);
Vue.use(Checkbox);
Vue.use(Table);
Vue.use(TableColumn);
Vue.use(Radio);
Vue.use(RadioGroup);
Vue.component(CollapseTransition.name, CollapseTransition,)
new Vue({
  router,
  store,
  render: h => h(App),
  beforeCreate(){
    Vue.prototype.$bus=this
  }
}).$mount('#app')
