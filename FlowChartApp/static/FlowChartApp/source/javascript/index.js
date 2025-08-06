import { createApp } from 'vue'
import FlowChartApp from '../vue_page/index.vue'
import PublicPlugins from '@components/static/assets/javascript/PublicPlugins.js'

window.app = createApp(FlowChartApp)
app = app.use(PublicPlugins)
