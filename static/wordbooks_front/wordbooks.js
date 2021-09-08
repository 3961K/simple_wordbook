Vue.mixin({ delimiters: ["${", "}"] });

const app = new Vue({
    el: '#app',
    data: {
        q: '',
        wordbooks_per_page: [],
        wordbooks_display_status: [],
        current_page_num: 0,
        next_page: false,
        previous_page: false,
    },
    created: async function() {
        // カードを取得する
        this.get_wordbooks_per_page(1);
    },
    methods: {
        get_wordbooks_per_page: function(page_number, with_q=false) {
            // そのユーザが作成したカードの一覧を取得する
            let params = {page: page_number};
            if (with_q) {
                params['q'] = this.q;
            }
            axios.get(
                `/api/v1/wordbooks/`,
                {
                    params: params
                }
            )
            .then(response => {
                if (response.status == 200){
                    this.wordbooks_per_page = response.data.results;
                    this.wordbooks_display_status = Array(this.wordbooks_per_page.length);
                    this.wordbooks_display_status.fill(true);
                    this.current_page_num = page_number;
                    this.next_page = response.data.next;
                    this.previous_page = response.data.previous;
                }
            })
            .catch(error => {
                // ステータスコードが2XXでなかった場合はalertでエラー内容を表示
                window.alert(error.response.data);
            })
        },
    },
    computed: {
        wordbook_display_status: function() {
            // 指定したカードの表示状態を返す
            return function(index) {
                return this.wordbooks_display_status[index];
            }
        },
        wordbook_content: function() {
            // 指定したカードの表示状態に基づいてwordまたはanswerを返す
            return function(index) {
                this.wordbooks_display_status.splice(index, 1, !this.wordbooks_display_status[index]);
            }
        }
    }
})