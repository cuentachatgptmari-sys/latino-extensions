pluginManagement {
    repositories {
        gradlePluginPortal()
        google()
        mavenCentral()
        maven("https://jitpack.io")
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.PREFER_SETTINGS)
    repositories {
        google()
        mavenCentral()
        maven("https://jitpack.io")
    }
}

rootProject.name = "latino-extensions"

include(
    ":PelisplushдProvider",
    ":CinecalidadProvider",
    ":GnulaProvider",
    ":CliverProvider",
    ":Cuevana3Provider",
    ":RepelisplusProvider",
    ":MegadedeProvider",
    ":PeliCineHDProvider",
    ":FilmapikProvider",
    ":SeriesdankoProvider",
    ":LaMovieProvider",
    ":PelisplusProvider",
    ":Series24Provider",
    ":TopstreamfilmProvider",
    ":NetcinezProvider",
    ":CoflixProvider",
    ":LatanimeProvider",
    ":GoojaraProvider",
    ":IdlixProvider"
)
