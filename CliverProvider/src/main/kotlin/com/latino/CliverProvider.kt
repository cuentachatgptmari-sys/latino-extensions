package com.latino

import com.lagradost.cloudstream3.*
import com.lagradost.cloudstream3.utils.*
import org.jsoup.nodes.Element

class CliverProvider : MainAPI() {
    override var mainUrl = "https://cliver.mom"
    override var name = "Cliver"
    override var lang = "es"
    override val hasMainPage = true
    override val hasSearch = true
    override val supportedTypes = setOf(TvType.Movie, TvType.TvSeries)

    override suspend fun getMainPage(page: Int, request: MainPageRequest): HomePageResponse {
        val doc = app.get(mainUrl).document
        val items = doc.select("article.TPost").mapNotNull { it.toSearchResult() }
        return newHomePageResponse("Inicio", items)
    }

    private fun Element.toSearchResult(): SearchResponse? {
        val title = selectFirst("h2.Title")?.text() ?: return null
        val href = selectFirst("a")?.attr("href") ?: return null
        val poster = selectFirst("img")?.attr("src")
        return newMovieSearchResponse(title, href, TvType.Movie) {
            this.posterUrl = poster
        }
    }

    override suspend fun search(query: String): List<SearchResponse> {
        val doc = app.get("$mainUrl?s=$query").document
        return doc.select("article.TPost").mapNotNull { it.toSearchResult() }
    }

    override suspend fun load(url: String): LoadResponse {
        val doc = app.get(url).document
        val title = doc.selectFirst("h1.Title")?.text() ?: ""
        val poster = doc.selectFirst("div.TPostBg img")?.attr("src")
        val desc = doc.selectFirst("div.Description p")?.text()
        return newMovieLoadResponse(title, url, TvType.Movie, url) {
            this.posterUrl = poster
            this.plot = desc
        }
    }

    override suspend fun loadLinks(data: String, isCasting: Boolean, subtitleCallback: (SubtitleFile) -> Unit, callback: (ExtractorLink) -> Unit): Boolean {
        val doc = app.get(data).document
        doc.select("div.TPlayer iframe").forEach {
            loadExtractor(it.attr("src"), data, subtitleCallback, callback)
        }
        return true
    }
}
