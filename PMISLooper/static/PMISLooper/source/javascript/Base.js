import { createApp } from 'vue'
import BaseApp from '../vue_page/Base.vue'
import PublicPlugins from '@components/static/assets/javascript/PublicPlugins.js'

window.app = createApp(BaseApp)
app = app.use(PublicPlugins)