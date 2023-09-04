# leptos_llama

Created: 2023-09-03 17:49

## 專案概述

![Pasted image 20230903173646.png](./pic/Pasted%20image%2020230903173646.png)
使用的[模型](https://huggingface.co/TheBloke/Wizard-Vicuna-7B-Uncensored-GGML/blob/main/Wizard-Vicuna-7B-Uncensored.ggmlv3.q8_0.bin)
![Pasted image 20230903173655.png](./pic/Pasted%20image%2020230903173655.png)
我們直接下載下來的檔案，只是模型的權重，我們需要使用套件來讀取並使用這些權重
![Pasted image 20230903173716.png](./pic/Pasted%20image%2020230903173716.png)
我們將使用llm這個套件來進行模型的處理

![Pasted image 20230903173728.png](./pic/Pasted%20image%2020230903173728.png)我們還需要leptos，這是一個包含前後端的框架，基於WASM技術之上的，讓我們可以進行Full stack開發

![Pasted image 20230903173745.png](./pic/Pasted%20image%2020230903173745.png)而且leptos的效能很好，贏過很多目前主流的前端架構，包含Vue、React，不過輸給Solid，Solid可以說是目前效能最好的前端框架

### 前置作業

![Pasted image 20230903173756.png](./pic/Pasted%20image%2020230903173756.png)首先要安裝WASM套件

![Pasted image 20230903173819.png](./pic/Pasted%20image%2020230903173819.png)接著安裝[trunk](https://trunkrs.dev/)跟[cargo-leptos](https://leptos.dev/)，trunk負責將我們的內容打包送到前端去，也提供local hosting的功能，這是web development必備的，當我們更改前端的內容時，他會同步更新顯示的畫面（hot-reloading），而cargo-leptos則做到相同的事，在我們更改後端服務時，他會hot-reloading將更新內容更新到服務上

![Pasted image 20230903173829.png](./pic/Pasted%20image%2020230903173829.png)安裝後我們使用cargo-leptos來新增專案
**這邊留意cargo-leptos跟leptos不太一樣，cargo-leptos是leptos的build tool（用於自動化建置（build）過程），就像cargo那樣。**
並指定一個git專案，指定專案的用意是讓我們可以直接套用模板，並輸入專案名稱rusty_llama，按下enter就可以了
作者的版本是trunk = 0.17.1跟cargo-leptos = 0.1.11，我則是trunk = 0.17.5跟cargo-leptos = 0.1.11

![Pasted image 20230903173841.png](./pic/Pasted%20image%2020230903173841.png)接著我們切換到該目錄底下，並使用指令

```sh
cargo leptos watch
```

來對該專案的變更進行監控
>這邊一個卡關，因為leptos升級至4.10，讓我的cargo-leptos建立不起來了，目前打算去修改cargo.toml看能不能處理
>![[Screenshot 2023-09-03 at 6.33.06 PM.png]]後來發現是site.start().line()多了()導致無法啟動，去除之後就可以使用了
>後來leptos回覆，説只要rust更新就可以正常使用了

```sh
rust update nightly
```

![Pasted image 20230903173921.png](./pic/Pasted%20image%2020230903173921.png)然後到瀏覽器輸入localhost:3000，就可以看到一個簡易的Web畫面，那個就是我們套用的模板

![Pasted image 20230903173934.png](./pic/Pasted%20image%2020230903173934.png)接著我們打開app.rs，然後修改HomePage function的內容，將`Welcome to Leptos!`改成任意你想要的文字，儲存出去之後，可以看到畫面有即時的變更，這就是hot-reloading的威力！！

![Pasted image 20230903173950.png](./pic/Pasted%20image%2020230903173950.png)接著來看一下專案目錄，這邊包含了我們前後端所需要的東西，app.rs是前端的entry point，而main.rs是後端的entry point，後端的部分我們也可以使用actix、axum來抽換

![Pasted image 20230903174004.png](./pic/Pasted%20image%2020230903174004.png)點開main.rs這邊可以看到兩個cfg屬性，一個是ssr，一個是csr，ssr表示只有在後端build的時候才會一起build（Server-side rendering: Generate an HTML string (typically on the server)），而csr（Client-side rendering: Generate DOM nodes in the browser）則相反，表示只有在前端build的時候才會一起build，這可以幫助我們控管依賴，這相當重要，因為很多crate是沒辦法用WASM的方式build起來（像是actix，你總不會把網頁後端也打包送過去吧），透過ssr, csr，我們可以prune依賴圖，根據我們今天要build前端還是後端，舉例來說，我們今天要build前端，我們不需要actix，透過這個屬性的設置，就可以避免使用所有依賴

![Pasted image 20230903174018.png](./pic/Pasted%20image%2020230903174018.png)我們打開cargo.toml，可以看到dependencies的部分，actix-web的部分是optional的，再看到features部分的csr，可以看到actix沒有列在其中，而是列在ssr的部分，這將前後端所需的crate區分，只有在build前端的時候，前端的crate才會一併build，反之亦然

![Pasted image 20230903174033.png](./pic/Pasted%20image%2020230903174033.png)我們前端css的部分，將使用Tailwind來設置

![Pasted image 20230903174047.png](./pic/Pasted%20image%2020230903174047.png)我們畫面的部分主要區分三大component，分別是訊息區塊、prompt輸入區塊跟畫面區塊，畫面區塊是所有的基底，訊息跟prompt都是在畫面之上去呈現的

![Pasted image 20230903174108.png](./pic/Pasted%20image%2020230903174108.png)在這個專案中，我們不需要HomePage component，也不需要router，因此我們可以直接刪除，並先加上ChatArea跟TypeArea，變成如圖下這樣
![Pasted image 20230903174118.png](./pic/Pasted%20image%2020230903174118.png)
![Pasted image 20230903174129.png](./pic/Pasted%20image%2020230903174129.png)接著我們要建立一個module叫做model，並在裡面建立conversation.rs，用來擺放我們定義的資料物件，以及mod.rs，來將conversation include到裡面

![Pasted image 20230903174142.png](./pic/Pasted%20image%2020230903174142.png)接著再回到外層的lib.rs，引入module model

![Pasted image 20230903174152.png](./pic/Pasted%20image%2020230903174152.png)再回到conversation.rs，現在要來實作conversation struct，但在此之前，我們先來實作message struct

![Pasted image 20230903174232.png](./pic/Pasted%20image%2020230903174232.png)我們先定義Message，有兩個屬性user跟text，user是bool，用來表示該訊息是user發出的，還是llm模型回應的，然後是text，這是訊息的文字。
接著我們實作Conversation，有一個屬性messages，是一個Vector裡面存放的是Message物件，也就是聊天記錄。
由於這兩個物件都需要能夠序列化、反序列化成JSON，所以我們需要使用serde這個套件，以及其derive feature，安裝指令是

```rust
cargo add serde -F derive
```

安裝後我們就可以對兩個物件進行derive，同時我們也需要能夠複製跟Debug print，所以也加上Clone跟Debug屬性。
最後，為了方便Conversation的建立，我們幫conversation實作`fn new` 來快速創建這個物件。

![Pasted image 20230903174300.png](./pic/Pasted%20image%2020230903174300.png)我們需要創建signal物件，signal物件會回傳一個tuple物件包含兩個elements，一個是ReadSignal，一個用來WriteSignal，如果我需要讀取資料，就對ReadSignal做事，如果需要更新資料，就對WriteSignal做事。這邊我們將Conversation物件傳入，用意是每當要更新資訊時，我們是更新我們傳入的Conversation物件

![Pasted image 20230903174312.png](./pic/Pasted%20image%2020230903174312.png)建立action，action是指使用者在做特定行為之後，連帶觸發的一系列邏輯。
在這裡，該特定行為是使用者輸入文字後點選submit button，我們將會把訊息建立成一個Message物件，並透過WriteSignal更新到conversation裡面，然後，我們將conversation設在ChatArea之後，代表當conversation更新，畫面顯示也要跟著更新。

![Pasted image 20230903174324.png](./pic/Pasted%20image%2020230903174324.png)在src底下建立api.rs，用來放置所有server端的function，但在開始撰寫邏輯之前，先回到lib.rs，將api module引入

![Pasted image 20230903174339.png](./pic/Pasted%20image%2020230903174339.png)開始撰寫我們的第一隻function，這是一個async function，他會接受上下文物件、Conversation當作參數，然後回傳Result，成功的話是String，錯誤的話是ServerFnError，function裡面會use一些套件。
leptos很棒的一點是，你定義的方法，在前端那邊可以直接使用，leptos會幫你呼叫HTTP來調用，我們不需要自己去實作那部分的邏輯，可以專注在function的使用設計上就好
可以看到我們的function上面有`#[server(Converse "api")]` ，這段是宣告說下面這個方法是server端的方法，當ssr被開啟時，這段才會被啟用，若是從client端呼叫此方法，即csr或hydrate有開啟時，並不是呼叫此方法，取而代之是發出一個request到server上，Converse是這個方法的名稱，"api"則是這個方法的URL prefix，我們這邊沒有特別指定這個方法的URL是什麼是因為前端那邊知道這個方法的路徑並可以直接呼叫，我們就不需要額外定義，且leptos會幫我們生成一個unique path給這個方法

![Pasted image 20230903174356.png](./pic/Pasted%20image%2020230903174356.png)會到Cargo.toml，將 [llm](https://github.com/rustformers/llm)加入依賴，並在ssr那邊標示llm是後端才需要的依賴

![Pasted image 20230903174406.png](./pic/Pasted%20image%2020230903174406.png)如果你熟知actix-web，你可能知道Extractor，簡單來說Extractor可以幫你將HTTP的部分拆解，讓你可以獲得HTTP資料的各個Part，而我們也可以透過Extractor讓server端的邏輯share共通的資料，這點很重要，因為我們是建立在actix這個框架，所以我們沒辦法explicitly的表明要傳遞什麼參數，而是必須透過actix的設計來進行傳遞，而在actix，這資料稱為"App Data"
Data裡面物件為Llama，Llama是一個llm物件包含我們讀取的model，呼叫into_inner()讓我們extract該data wrapper，into_inner後的分號是誤加的

![Pasted image 20230903174420.png](./pic/Pasted%20image%2020230903174420.png)提供對話情境，讓llm模型可以inference，每句前面都會加上三個#字號，然後是Assistant表示模型，Human代表我們，在最後要給模型inference的部分，我們記上Assistant，表示後面是模型要進行預測的部分

![Pasted image 20230903174429.png](./pic/Pasted%20image%2020230903174429.png)迭代每個過去的訊息，並根據訊息的角色添加前綴加入歷史訊息

![Pasted image 20230903174440.png](./pic/Pasted%20image%2020230903174440.png)這邊有使用到rand，要記得到Cargo.toml加上依賴，ssr的部分也要記得添加。
在正式環境，你可能會儲存session以達到更好的效率，但這邊我們每次都重新產生一個session。
這邊在做的事，是讓模型進行inference，我們給予模型、隨機數、InferenceRequest、預設output request、callback作為參數

- 模型是要用來進行推論的模型
- 隨機數是讓結果有隨機性，每次都不一樣
- InferenceRequest會接受
- prompt來告訴模型他要推論的內容
- 初始的參數
- 是否要對之前接受的token呼叫callback，我們的情況，每次session都會刷新，所以設為false
- token的最大產出數量
- OutputRequest不確定是什麼
- callback方法是用來告訴模型什麼時候要停止，不然模型會不斷的往下預測，這邊的停止條件是當模型輸出Human的時候
注意：parameter的Some是錯的，需要去掉，以及最後要回傳的是Ok(res)而不是空String

![Pasted image 20230903174502.png](./pic/Pasted%20image%2020230903174502.png)
![Screenshot 2023-09-03 at 10.22.09 PM.png](./pic/Screenshot%202023-09-03%20at%2010.22.09%20PM.png)這邊沒有多做說明，只有說這是用來讓模型用來判斷是否停止的邏輯
這邊留意，我們提供的public api是沒有進行驗證、權限檢查的等等的，如果有要production的話，記得要加上去

![Pasted image 20230903174544.png](./pic/Pasted%20image%2020230903174544.png)回到main.rs加上加載model的部分，這邊使用dotenv這個套件來讀取環境變數，然後得知我們模型下載的位置，當然如果求方便，直接使用寫死的路徑也可以，如果有用dotenv的話，記得到Cargo.toml去添加依賴。

然後呼叫llm提供的關聯函數來讀取模型，如果有錯的話直接panic關閉服務。

這邊我們不能用過去的作法，透過設定feature來表示ssr，而必須使用cfg_if，是因為我們需要函數回傳是Llma，我們必須在fn上面添加use，先將Llma引入，所以才必須寫得像這樣，當然可能會覺得為什麼不把所有use都寫到最上面，當然可以，但這會使作用域變得太臃腫，而且在laptos中有區分前後端，可以分別啟動，如果單一邊啟動就必須加載所有的依賴，那也太浪費資源了。

![Pasted image 20230903174559.png](./pic/Pasted%20image%2020230903174559.png)這邊加上model，是一個上下文物件，用來共享使用的，我們用actix提供的Data struct將model包裝在裡面，這個Data底層是atomic的reference，可以讓我們在多執行緒的情況下也做到安全的共享

![Pasted image 20230903174608.png](./pic/Pasted%20image%2020230903174608.png)添加css函數，並添加到service上，讓外界可以讀取到我們的Tailwind css

![Pasted image 20230903174619.png](./pic/Pasted%20image%2020230903174619.png)回到Cargo.toml，我們添加一個section，這個section講者也不知道在幹嘛，但添加可以加快本機的運算速度

![Pasted image 20230903174629.png](./pic/Pasted%20image%2020230903174629.png)添加converse函數，將所需的上下文、內容作為參數，converse是我們在server實作的函數，不過我們在前端這邊也可以直接使用並呼叫，leptos會自動識別，相當方便

![Pasted image 20230903174639.png](./pic/Pasted%20image%2020230903174639.png)添加create_effect監聽，當使用者輸入文字時，會在畫面上出現“...”來表示正在回應中。

![Pasted image 20230903174653.png](./pic/Pasted%20image%2020230903174653.png)再添加一個監聽，當server回應時，將文字更新到畫面上。

![Pasted image 20230903174705.png](./pic/Pasted%20image%2020230903174705.png)接著來實作ChatArea畫面的部分，這邊建立component這個module，並生成三個檔案mod.rs、chat_area.rs、type_area.rs。
來到chat_area，首先使用到component這個macro，這個macro可以將我們寫的函數轉換成前端物件。

我們提供參數，cx：上下文、conversation：ReadSignal，並回傳IntoView，畫面的細節先不管，回傳的內容是從conversation裏面遍歷出來，並根據訊息是user還是model回覆的進行tailwind css的風格調整。這邊都是使用閉包，我猜想應該是因為畫面的渲染是動態的，所以要給view!一個閉包函數，讓他來做調用

![Pasted image 20230903174723.png](./pic/Pasted%20image%2020230903174723.png)接著使用create node ref，這個函數將建立一個DOM node 的 reference，讓你能夠直接修改那個node（前端我沒很懂），這個ref我們要用來更新畫面，當聊天視窗有新訊息加入時，我們要確保畫面會一直保持在最上方（在討論畫面時，上方指的是下面，而下方指的是上面，這跟座標有關，(0,0)是在左下方）。

![Pasted image 20230903174734.png](./pic/Pasted%20image%2020230903174734.png)最後是TypeArea的部分，我們創建Input的ref，並添加閉包函數，當觸發submit時，我們會將訊息傳遞到後端，並刷新輸入框，這邊可以看到prevent_default，這是用來將submit這個buttom的預設事件關閉，也就是將跳轉取消，這樣訊息依然可以傳遞，但畫面不會跳轉。

然後加上node_ref，這用來標記我們要ref哪個物件，ChatArea那邊也要記得添加。

![Pasted image 20230903174748.png](./pic/Pasted%20image%2020230903174748.png)建立input.css

![Pasted image 20230903174758.png](./pic/Pasted%20image%2020230903174758.png)cargo.toml這邊，將style-file改成"style/ouput.css"，等等我們會用tailwindcss將input.css編譯成output.css
  
![Pasted image 20230903230647.png](./pic/Pasted%20image%2020230903230647.png)編譯tailwind

最後

```sh
cargo leptos watch
```

## 重要

**此專案為參考大老影片並由我記錄下來的筆記，如有問題絕對是我紀錄錯誤**

---

## References

[video](https://www.youtube.com/watch?v=vAjle3c9Xqc)
