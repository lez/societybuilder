var gulp = require('gulp');
var react = require('gulp-react');
var concat = require('gulp-concat');
var source = require('vinyl-source-stream');
var browserify = require('browserify');
var watchify = require('watchify');
var reactify = require('reactify');
var streamify = require('gulp-streamify');

var JS_DEST_DIR = '../ist/static/js';
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


gulp.task('watch', function() {
  var watcher  = watchify(browserify({
        entries: JS_ENTRYPOINTS,
          transform: [reactify],
          debug: true,
          cache: {}, packageCache: {}, fullPaths: true
      }));

  watcher.on('update', function () {
      watcher.bundle()
        .pipe(source(JS_BUNDLE))
        .pipe(gulp.dest(JS_DEST_DIR));
        console.log('Updated');
  }).bundle()
    .pipe(source(JS_BUNDLE))
    .pipe(gulp.dest(JS_DEST_DIR));
});

gulp.task('css', function () {
    gulp.watch(CSS_FILES, function () {
        return gulp.src(CSS_FILES)
        .pipe(concat(CSS_BUNDLE))
        .pipe(gulp.dest(CSS_DEST_DIR));
    });
});


gulp.task('default', ['watch', 'css']);
