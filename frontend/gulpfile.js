var gulp = require('gulp');
var react = require('gulp-react');
var concat = require('gulp-concat');
var source = require('vinyl-source-stream');
var browserify = require('browserify');
var watchify = require('watchify');
var reactify = require('reactify');
var streamify = require('gulp-streamify');






gulp.task('transform', function() {
    gulp.src('react_components/App.jsx')
        .pipe(react())
        .pipe(gulp.dest('dist'));
});

gulp.task('watchsingle', function(){
    gulp.watch('react_components/App.jsx', ['transform']);
});


gulp.task('prod', function(){
    gulp.src('react_components/App.jsx')
      .pipe(react())
      .pipe(concat('dist/app.min.js'))
      .pipe(gulp.dest('.'));
});


gulp.task('watch', function() {
  var watcher  = watchify(browserify({
        entries: ['react_components/App.jsx'],
          transform: [reactify],
          debug: true,
          cache: {}, packageCache: {}, fullPaths: true
      }));
  return watcher.on('update', function () {
        watcher.bundle()
          .pipe(source('app.big.js'))
          .pipe(gulp.dest('dist'))
          console.log('Updated');
    })
   .bundle()
      .pipe(source('build.js'))
      .pipe(gulp.dest('dist/src'));
});
