var  path = require( 'path' )
export default{
   build: {
     index: path.resolve(__dirname,  'dist/index.html' ),
     assetsRoot: path.resolve(__dirname,  'dist' ),
     assetsSubDirectory:  'static' ,
     assetsPublicPath:  '/' ,
     productionSourceMap:  true
   },
   dev: {
     port: 8080,
     proxyTable: {}
   },
    publicPath:process.env.NODE_ENV === "production" ?"./":"/",
}