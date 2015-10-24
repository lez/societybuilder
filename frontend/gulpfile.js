var gulp = require('gulp');
var react = require('gulp-react');
var concat = require('gulp-concat');
var source = require('vinyl-source-stream');
var browserify = require('browserify');
var watchify = require('watchify');
var reactify = require('reactify');
var streamify = require('gulp-streamify');
var gutil = require('gulp-util');
var browserSync = require('browser-sync').create();


var JS_DEST_DIR = '../ist/static/js/compiled';
var JS_BUNDLE = 'app.js';
var JS_ENTRYPOINTS = ['react_components/App.jsx'];

var CSS_DEST_DIR = '../ist/static/style';
var CSS_BUNDLE = 'bundle.css';
var CSS_FILES = ['react_components/*.css', 'common_css/*.css', '../ist/static/fontello/css/is-codes.css'];

//gulp.task('transform', function() {
//    gulp.src('react_components/App.jsx')
//        .pipe(react())
//        .pipe(gulp.dest('dist'));
//});

gulp.task('prod', function(){
    gulp.src('react_components/App.jsx')
      .pipe(react())
      .pipe(concat('dist/app.min.js'))
      .pipe(gulp.dest('.'));
});


gulp.task('watch_js', function() {
  var watcher = watchify(browserify({
        entries: JS_ENTRYPOINTS,
        transform: [reactify],
        debug: false,
        cache: {},
        packageCache: {},
        fullPaths: true
  }));

  watcher.on('log', gutil.log.bind(gutil, 'JS'));
  watcher.on('update', function (event) {
      watcher.bundle()
        .on('error', gutil.log.bind(gutil, 'Browserify error'))
        .pipe(source(JS_BUNDLE))
        .pipe(gulp.dest(JS_DEST_DIR));
      gutil.log('JS changed: ' + event);
  }).bundle()
    .on('error', gutil.log.bind(gutil, 'Browserify error 2'))
    .pipe(source(JS_BUNDLE))
    .pipe(gulp.dest(JS_DEST_DIR));
});

gulp.task('watch_css', function () {
    gulp.watch(CSS_FILES, function (event) {
        gutil.log('CSS changed: ' + event.path);
        return gulp.src(CSS_FILES)
            .on('error', gutil.log.bind(gutil, 'CSS error'))
            .pipe(concat(CSS_BUNDLE))
            .pipe(browserSync.stream({match: "**/*.css"}))
            .pipe(gulp.dest(CSS_DEST_DIR));
    });
});

gulp.task('serve_browsersync', function () {
    // Proxy files, reload if js bundle changes
    browserSync.init({
        proxy: 'cb.dev'
    });
    gulp.watch(JS_DEST_DIR + '/' + JS_BUNDLE).on("change", browserSync.reload);
});


gulp.task('default', ['watch_js', 'watch_css', 'serve_browsersync']);
