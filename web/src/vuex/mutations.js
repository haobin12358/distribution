import {SAVE_READING_MESSAGE} from './mutation-types'

export default {
    [SAVE_READING_MESSAGE](state,msg){
        state.readingMessage = msg;
    }
}
