package com.latino

import com.lagradost.cloudstream3.plugins.CloudstreamPlugin
import com.lagradost.cloudstream3.plugins.Plugin
import android.content.Context

@CloudstreamPlugin
class PelisplushдProvider : Plugin() {
    override fun load(context: Context) {
        registerMainAPI(Pelisplushd())
        registerExtractorAPI(FileMoonlink())
        registerExtractorAPI(Mivalyo())
        registerExtractorAPI(StreamwishHG())
    }
}
