/**
 * Created by Ken on 8/14/2015.
 */
module.exports = function(grunt) {
        grunt.initConfig({
            pkg: grunt.file.readJSON('package.json'),
            uglify: {
                options: {
                    banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
                },
                build: {
                    src: 'src/<%= pkg.name %>.js',
                    dest: 'build/<%= pkg.name %>.min.js'
                }
            }
        });

    // Load the plugin that provides tasks
    grunt.loadNpmTasks('grunt-contrib-uglify');

    // Default tasks.
    grunt.registerTask('default', ['uglify']);

};