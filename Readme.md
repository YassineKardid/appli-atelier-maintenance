### install NodeJS
    
        curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
        sudo apt-get install -y nodejs

### create new project angular

        sudo npm install -g @angular/cli
        ng new frontend
        cd frontend
        ng serve

### install rxjs
        
        npm install --save rxjs-compat  Observable
        npm install --save-dev @angular-devkit/build-angular (?)

### install MD

        npm install --save @angular/material @angular/cdk @angular/animations        
        ng add @angular/material
        import {BrowserAnimationsModule} from '@angular/platform-browser/animations';

### install MD datepickerRange  https://www.npmjs.com/package/ngx-daterangepicker-material

        npm install ngx-daterangepicker-material --save
        npm install moment --save

### install scroll bar  https://www.npmjs.com/package/ngx-scrollbar
### example https://stackblitz.com/edit/ngx-scrollbar?file=src%2Fapp%2Fhome%2Fhome.component.html

        npm i -S ngx-scrollbar @angular/cdk



        npm install --save @ng-bootstrap/ng-bootstrap

        