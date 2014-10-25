#!/bin/sh

if
main.sbin check_admin_session
then
eval `cat $DOCUMENT_ROOT/apps/aria2/i18n/$(main.sbin get_client_lang)/i18n.conf`
else
main.sbin header_jump "/index.cgi?app=login" && exit 1
fi

cat <<EOF
<!DOCTYPE html>
<!--
  Copyright (C) 2012 Binux <17175297.hk@gmail.com>

  This file is part of YAAW (https://github.com/binux/yaaw).

  YAAW is free software: you can redistribute it and/or modify
  it under the terms of the GNU Lesser General Public License as
  published by the Free Software Foundation, either version 3 of
  the License, or (at your option) any later version.

  YAAW is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU Lesser General Public License for more details.

  You may get a copy of the GNU Lesser General Public License
  from http://www.gnu.org/licenses/lgpl.txt
-->
<html lang="en" manifest="offline.appcache">
  <head>
    <meta charset=utf-8 />
    <title>Yet Another Aria2 Web Frontend</title>
    <meta name="viewport" content="initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no, width=device-width">
    <meta name="author" content="Binux" />
    
    <link href="img/favicon.ico" rel="shortcut icon" type="image/ico" />
    <link href="css/bootstrap.min.css" rel="stylesheet" />
    <link href="css/bootstrap-responsive.min.css" rel="stylesheet" />
    <link href="css/main.css" rel="stylesheet" />
    <!--[if lt IE 9]>
      <script src="//html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
  </head>
  <body>
    <div class="container">
      <header class="main-head page-header">
        <h1>Yet Another Aria2 Web Frontend</h1>
        <span id="offline-cached"></span>
        <div id="global-info" class="pull-right">
          <div id="global-version"></div>
          <div id="global-speed"></div>
        </div>
      </header>

      <div class="clearfix hide" id="main-control">
        <div id="main-alert" class="hide">
          <div id="main-alert-inline" class="alert">
            <a href="###" onclick="\$('#main-alert').hide();" class="close">×</a>
            <span class="alert-msg">$_LANG_Loading</span>
          </div>
        </div>

        <div class="pull-left">
          <div class="btn-group" id="select-btn">
            <button id="select-all-btn" class="btn" rel="tooltip" title="$_LANG_Select_All">
              <i class="select-box"></i>
            </button>
            <a class="btn dropdown-toggle" data-toggle="dropdown" href="#">
              <span class="caret"></span>
            </a>
            <ul class="dropdown-menu">
			<li><a href="###" onclick="YAAW.tasks.selectActive();">$_LANG_Select_Active</a></li>
              <li><a href="###" onclick="YAAW.tasks.selectWaiting();">$_LANG_Select_Waiting</a></li>
              <li><a href="###" onclick="YAAW.tasks.selectPaused();">$_LANG_Select_Paused</a></li>
              <li><a href="###" onclick="YAAW.tasks.selectStoped();">$_LANG_Select_Stoped</a></li>
            </ul>
          </div>
        </div>

        <div class="pull-left" id="not-selected-grp">
          <div class="pull-left btn-group">
            <a class="btn" id="add-task-btn" data-toggle="modal" href="#add-task-modal" rel="tooltip" title="$_LANG_Add_Task">
              <i class="icon-plus"></i> $_LANG_Add
            </a>
          </div>
          <div class="pull-left btn-group" id="do-all-btn">
            <a href="###" onclick="ARIA2.unpause_all();" class="btn" id="unpause-all" rel="tooltip" title="Start All">
              <i class="icon-forward"></i>
            </a>
            <a href="###" onclick="ARIA2.pause_all();" class="btn" id="pause-all" rel="tooltip" title="Pause All">
              <i class="icon-stop"></i>
            </a>
            <a href="###" onclick="ARIA2.purge_download_result();" class="btn" id="pure-all" rel="tooltip" title="Remove Finished Tasks">
              <i class="icon-trash"></i>
            </a>
          </div>
        </div>

        <div class="pull-left hide" id="selected-grp">
          <div class="btn-group">
            <a href="###" onclick="YAAW.tasks.unpause();YAAW.tasks.unSelectAll();" class="btn" rel="tooltip" title="Start">
              <i class="icon-play"></i>
            </a>
            <a href="###" onclick="YAAW.tasks.pause();YAAW.tasks.unSelectAll();" class="btn" rel="tooltip" title="Pause">
              <i class="icon-pause"></i>
            </a>
            <a href="###" onclick="YAAW.tasks.remove();YAAW.tasks.unSelectAll();" class="btn" rel="tooltip" title="Remove">
              <i class="icon-remove"></i>
            </a>
          </div>
          <!--<button class="btn pull-left" id="info-btn" rel="tooltip" title="Task Info">-->
            <!--<i class="icon-info-sign"></i> Info-->
          <!--</button>-->
        </div>

        <div class="pull-right" id="other-grp">
          <div class="btn-group">
            <a href="#" class="btn" id="refresh-btn" rel="tooltip" title="$_LANG_Refresh">
              <i class="icon-refresh"></i> $_LANG_Refresh
            </a>
            <a class="btn" id="setting-btn" data-toggle="modal" href="#setting-modal" rel="tooltip" title="$_LANG_Settings">
              <i class="icon-wrench"></i>
            </a>
          </div>
        </div>
      </div>

      <section id="active-tasks">
      <div class="section-header">
        <i class="icon-chevron-down"></i><b>$_LANG_Active_Tasks</b>
      </div>
      <ul class="tasks-table" id="active-tasks-table">
        <li>
          <div class="empty-tasks">
            <strong>$_LANG_No_Active_Tasks</strong>
          </div>
        </li>
      </ul>
      </section>

      <section id="other-tasks">
      <div class="section-header">
        <i class="icon-chevron-down"></i><b>$_LANG_Other_Tasks</b>
      </div>
      <ul id="waiting-tasks-table" class="tasks-table">
        <li>
          <div class="empty-tasks">
            <strong>$_LANG_No_Tasks</strong>
          </div>
        </li>
      </ul>
      <ul id="stoped-tasks-table" class="tasks-table"> </ul>
      </section>
    </div>

    <ul id="task-contextmenu" class="dropdown-menu">
      <li class="task-restart"><a href="###" onclick="YAAW.contextmenu.restart();">$_LANG_ReStart</a></li>
      <li class="task-start"><a href="###" onclick="YAAW.contextmenu.unpause();">$_LANG_Start</a></li>
      <li><a href="###" onclick="YAAW.contextmenu.pause();">$_LANG_Pause</a></li>
      <li><a href="###" onclick="YAAW.contextmenu.remove();">$_LANG_Remove</a></li>
      <li class="task-move divider"></li>
      <li class="task-move"><a href="###" onclick="YAAW.contextmenu.movetop();">$_LANG_MoveTop</a></li>
      <li class="task-move"><a href="###" onclick="YAAW.contextmenu.moveup();">$_LANG_MoveUp</a></li>
      <li class="task-move"><a href="###" onclick="YAAW.contextmenu.movedown();">$_LANG_MoveDown</a></li>
      <li class="task-move"><a href="###" onclick="YAAW.contextmenu.moveend();">$_LANG_MoveEnd</a></li>
    </ul>

    <section class="modal hide fade" id="add-task-modal">
    <div class="modal-header">
      <button class="close" data-dismiss="modal">×</button>
      <h3>$_LANG_Add_Task</h3>
    </div>
    <div class="modal-body">
      <div id="add-task-alert" class="alert alert-error hide">
        <a href="###" onclick="\$('#add-task-alert').hide();" class="close">×</a>
        <strong>$_LANG_Error :</strong> <span class="alert-msg"></span>
      </div>
      <form id="add-task-uri" onsubmit="YAAW.add_task.submit(this);return false;">
        <div class="input-append">
          <input type="text" name="uri" id="uri-input" class="input-clear" placeholder="HTTP, FTP or Magnet" /><span><a id="torrent-up-btn" class="btn">$_LANG_Upload_Torrent<input type="file" id="torrent-up-input" /></a></span>
        </div>
        <textarea id="uri-textarea" rows=5 class="input-clear hide" placeholder="HTTP, FTP or Magnet"></textarea>
      </form>
      <div id="uri-more"><span class="or-and">&or;&or;&or;&or;&or;&or;</span><span class="or-and" style="display:none;">&and;&and;&and;&and;&and;&and;</span></div>
      <div id="add-task-option-wrap"></div>
    </div>
    <div class="modal-footer">
      <a href="###" onclick="\$('#add-task-uri').submit();" id="add-task-submit" class="btn btn-primary">$_LANG_Add</a>
      <a href="###" onclick="YAAW.add_task.clean();" class="btn" data-dismiss="modal">$_LANG_Cancel</a>
    </div>
    </section>

    <section class="modal hide fade" id="setting-modal">
    <div class="modal-header">
      <button class="close" data-dismiss="modal">×</button>
      <h2>$_LANG_Settings</h2>
    </div>
    <div class="modal-body">
      <form id="setting-form" class="form-horizontal" onsubmit="YAAW.setting.submit();return false;">
        <fieldset>
          <div class="control-group rpc-path-group">
            <label class="control-label" for="rpc-path">$_LANG_JSON_RPC_Path</label>
            <div class="controls">
              <div class="input-append btn-group rpc-path-wrap">
                <input type="text" class="input-xlarge" id="rpc-path"><a class="add-on btn dropdown-toggle" href="#" disabled><b class="caret"></b></a>
              </div>
            </div>
          </div>
          <div class="control-group">
            <label class="control-label">$_LANG_Auto_Refresh</label>
            <div class="controls">
              <label class="radio inline">
                <input type="radio" name="refresh_interval" value="1000"> 1s
              </label>
              <label class="radio inline">
                <input type="radio" name="refresh_interval" value="5000" checked> 5s
              </label>
              <label class="radio inline">
                <input type="radio" name="refresh_interval" value="10000"> 10s
              </label>
              <label class="radio inline">
                <input type="radio" name="refresh_interval" value="60000"> 1min
              </label>
              <label class="radio inline">
                <input type="radio" name="refresh_interval" value="0"> off 
              </label>
            </div>
          </div>
        </fieldset>
      </form>
      <div id="aria2-gsetting">
      </div>
    </div>
    <div class="modal-footer">
      <div id="copyright">© Copyright <a href="https://github.com/binux/yaaw">Binux</a></div>
      <a href="###" onclick="\$('#setting-form').submit();" class="btn btn-success">$_LANG_Save</a>
      <a href="#" class="btn" data-dismiss="modal">$_LANG_Cancel</a>
    </div>
    </section>
    
    <script id="global-speed-tpl" type="text/mustache-template">
      <i class="icon-download"></i> <span>{{#_v.format_size}}{{downloadSpeed}}{{/_v.format_size}}</span>/s
        / 
      <i class="icon-upload"></i>  <span>{{#_v.format_size}}{{uploadSpeed}}{{/_v.format_size}}</span>/s
    </script>

    <script id="active-task-tpl" type="text/mustache-template">
      {{#tasks}}
      <li class="task" id="task-gid-{{gid}}" data-status="{{status}}" data-gid="{{gid}}">
        <div class="left-area">
          <div class="task-name">
            <i class="select-box"></i>
            <span title="{{title}}">{{title}}</span>
          </div>
          <div class="task-info">
            <span class="task-status" rel="tooltip" title="{{status}} {{#_v.error_msg}}{{errorCode}}{{/_v.error_msg}}"><i class="{{#_v.status_icon}}{{status}}{{/_v.status_icon}}"></i></span>
            <span>{{#_v.format_size}}{{completedLength}}{{/_v.format_size}} / {{#_v.format_size}}{{totalLength}}{{/_v.format_size}}</span>
            {{#uploadLength}}<span>(uploaded {{#_v.format_size}}{{uploadLength}}{{/_v.format_size}})</span>{{/uploadLength}}
            {{#eta}}<span>ETA: {{#_v.format_time}}{{eta}}{{/_v.format_time}}</span>{{/eta}}
          </div>
        </div>
        <div class="right-area">
          <div class="progress">
            <div class="bar" style="width: {{progress}}%">{{progress}}%</div>
          </div>
          <div class="progress-info">
            {{#downloadSpeed}}<span class="download-speed"><i class="icon-download"></i> {{#_v.format_size}}{{downloadSpeed}}{{/_v.format_size}}/s</span>{{/downloadSpeed}}
            {{#uploadSpeed}}<span class="upload-speed"><i class="icon-upload"></i> {{#_v.format_size}}{{uploadSpeed}}{{/_v.format_size}}/s</span>{{/uploadSpeed}}
            {{#connections}}<span class="seeders"><i class="icon-signal" rel="tooltip" title="Connections"></i> {{connections}}</span>{{/connections}}
            {{#numSeeders}}<span class="seeders"><i class="icon-magnet" rel="tooltip" title="Seeders"></i> {{numSeeders}}</span>{{/numSeeders}}
          </div>
        </div>
      </li>
      {{/tasks}}
      {{^tasks}}
      <li>
        <div class="empty-tasks">
          <strong>$_LANG_No_Active_Tasks</strong>
        </div>
      </li>
      {{/tasks}}
    </script>
    
    <script id="other-task-tpl" type="text/mustache-template">
      {{#tasks}}
      <li class="task" id="task-gid-{{gid}}" data-status="{{status}}" data-gid="{{gid}}" data-infohash="{{infoHash}}">
        <div class="left-area">
          <div class="task-name">
            <i class="select-box"></i>
            <span title="{{title}}">{{title}}</span>
          </div>
        </div>
        <div class="right-area">
          <div class="task-info pull-left">
            <span class="task-status" rel="tooltip" title="{{status}} {{#_v.error_msg}}{{errorCode}}{{/_v.error_msg}}"><i class="{{#_v.status_icon}}{{status}}{{/_v.status_icon}}"></i></span>
            <span>{{#_v.format_size}}{{totalLength}}{{/_v.format_size}}</span>
            {{#uploadLength}}<span>(up {{#_v.format_size}}{{uploadLength}}{{/_v.format_size}}){{/uploadLength}}
          </div>
          <div class="pull-right">
            <div class="progress">
              <div class="bar" style="width: {{progress}}%">{{progress}}%</div>
            </div>
          </div>
          <div class="clearfix"></div>
        </div>
      </li>
      {{/tasks}}
    </script>

    <script id="info-box-tpl" type="text/mustache-template">
      <div class="info-box" data-gid="{{gid}}">
        <div class="tabbable tabs-left">
          <ul class="nav nav-tabs">
            <li class="active"><a href="#ib-status" data-toggle="tab">$_LANG_Status</a></li>
            <li><a href="#ib-files" data-toggle="tab"><?php echo $LANG['Files'];?></a></li>
            <li><a id="ib-options-a" href="#ib-options" data-toggle="tab">$_LANG_Options</a></li>
            <li><a id="ib-peers-a" class="hide" style="display:none;" href="#ib-peers" data-toggle="tab">$_LANG_Peers</a></li>
          </ul>
          <div class="tab-content">
            <div class="tab-pane active" id="ib-status"> </div>
            <div class="tab-pane" id="ib-files"> </div>
            <div class="tab-pane" id="ib-options"> </div>
            <div class="tab-pane" id="ib-peers"> </div>
          </div>
        </div>
      </div>
    </script>      

    <script id="ib-status-tpl" type="text/mustache-template">
      <ul>
        <li><strong>$_LANG_Size: </strong>{{#_v.format_size}}{{totalLength}}{{/_v.format_size}} ({{numPieces}} @ {{#_v.format_size}}{{pieceLength}}{{/_v.format_size}})</li>
        <li><strong>$_LANG_Status: </strong>{{status}} {{error_msg}}</li>
        <li><strong>$_LANG_Dir: </strong>{{dir}}</li>
        {{#bittorrent}}
          {{#creationDate}}<li>Torrent Created At {{creationDate}}</li>{{/creationDate}}
          {{#comment}}<li><strong>Comment: </strong>{{comment}}</li>{{/comment}}
        {{/bittorrent}}
        <li class="bitfield"><strong>$_LANG_Bitfield: </strong>{{#_v.bitfield}}{{bitfield}}{{/_v.bitfield}}</li>
      </ul>
    </script>

    <script id="ib-files-tpl" type="text/mustache-template">
      <ul>
        <li id="ib-file-btn">
          <button id="ib-file-save" class="btn btn-primary">$_LANG_Save</button>
          <button id="ib-file-select" class="btn">$_LANG_Select_All</button>
          <button id="ib-file-unselect" class="btn">$_LANG_Unselect_All</button>
        </li>
        {{#files}}
        <li>
          <i class="select-box{{#selected}} icon-ok{{/selected}}" data-index="{{index}}"></i>
          <span class="ib-file-title">{{title}}</span>
          <span class="ib-file-size"> {{#_v.format_size}}{{completedLength}}{{/_v.format_size}} / {{#_v.format_size}}{{length}}{{/_v.format_size}}</span>
        </li>
        {{/files}}
      </ul>
    </script>

    <script id="ib-options-tpl" type="text/mustache-template">
      <form id="ib-options-form" class="form-horizontal" onsubmit="false">
      <ul>
        <li id="ib-options-btn">
          <button id="ib-options-save" class="btn btn-primary">$_LANG_Save</button>
        </li>
        <li><span>$_LANG_Download_Limit:</span><input name="max-download-limit" class="active-allowed" value="{{max-download-limit}}" /></li>
        <li><span>$_LANG_Upload_Limit:</span><input name="max-upload-limit" class="active-allowed" value="{{max-upload-limit}}" /></li>
        <li><span>$_LANG_Split:</span><input name="split" value="{{split}}" /></li>
        <li><span>$_LANG_Conn_per_Serv:</span><input name="max-connection-per-server" value="{{max-connection-per-server}}" /></li>
        <li><span>$_LANG_Min_Split_Size:</span><input name="min-split-size" value="{{min-split-size}}" /></li>
      </form>
    </script>

    <script id="ib-peers-tpl" type="text/mustache-template">
      {{#.}}
      <li><span class="ip_port">{{ip}}:{{port}} - <span class="peerid">{{#_v.format_peerid}}{{peerId}}{{/_v.format_peerid}}</span></span> <b>{{#_v.bitfield_to_percent}}{{bitfield}}{{/_v.bitfield_to_percent}}%</b> <i class="icon-download"></i>{{#_v.format_size}}{{downloadSpeed}}{{/_v.format_size}}/s <i class="icon-upload"></i>{{#_v.format_size}}{{uploadSpeed}}{{/_v.format_size}}/s</li>
      {{/.}}
    </script>

    <script id="other-task-empty" type="text/mustache-template">
      <li>
        <div class="empty-tasks">
          <strong>$_LANG_No_Tasks</strong>
        </div>
      </li>
    </script>

    <script id="add-task-option-tpl" type="text/mustache-template">
      <hr />
      <form id="add-task-option" class="form-horizontal" onsubmit="\$('#add-task-uri').submit();return false">
	  <input type="submit" style="position:fixed;top:0;visibility:hidden"/>
        <div class="control-group">
          <label class="control-label" for="ati-out">$_LANG_File_Name</label>
          <div class="controls">
            <input id="ati-out" class="input-xlarge input-clear" name="out" />
          </div>
        </div>
        <div class="control-group">
          <label class="control-label" for="ati-dir">$_LANG_Dir</label>
          <div class="controls">
            <input id="ati-dir" class="input-xlarge" name="dir" />
          </div>
        </div>
        <div class="clearfix"></div>
        <div class="control-group half">
          <div class="controls">
            <label class="checkbox">
              <input type="checkbox" name="pause" class="input-save" {{#pause}}checked{{/pause}} />
              $_LANG_Pause_When_Added
            </label>
          </div>
        </div>
        <div class="control-group half">
          <div class="controls">
            <label class="checkbox">
              <input type="checkbox" name="parameterized-uri" class="input-save" {{#parameterized-uri}}checked{{/parameterized-uri}} />
              $_LANG_Parameterized_URI
            </label>
          </div>
        </div>
        <div class="clearfix"></div>
        <div class="control-group half">
          <label class="control-label" for="ati-split">$_LANG_Split</label>
          <div class="controls">
            <input id="ati-split" class="input-small input-save" name="split" value="{{split}}" />
          </div>
        </div>
        <div class="control-group half">
          <label class="control-label" for="ati-cps">Conn/Serv</label>
          <div class="controls">
            <input id="ati-cps" class="input-small input-save" name="max-connection-per-server" value="{{max-connection-per-server}}" />
          </div>
        </div>
        <div class="control-group half">
          <label class="control-label" for="ati-sr">$_LANG_Seed_Ratio</label>
          <div class="controls">
            <input id="ati-sr" class="input-small input-save" name="seed-ratio" value="{{seed-ratio}}" />
          </div>
        </div>
        <div class="control-group half">
          <label class="control-label" for="ati-st">$_LANG_Seed_Time</label>
          <div class="controls">
            <input id="ati-st" class="input-small input-save" name="seed-time" value="{{seed-time}}" />
          </div>
        </div>
        <div class="clearfix"></div>
        <div class="control-group">
          <label class="control-label" for="ati-header">$_LANG_Header</label>
          <div class="controls">
            <textarea id="ati-header" class="input-xlarge input-save" name="header" warp="off">{{header}}</textarea>
          </div>
        </div>
      </form>
    </script>

    <script id="aria2-global-setting-tpl" type="text/mustache-template">
      <hr />
      <form id="aria2-gs-form" class="form-horizontal" onsubmit="false">
        <div class="control-group half">
          <label class="control-label" for="gsi-dl">$_LANG_Download_Limit</label>
          <div class="controls">
            <input id="gsi-dl" name="max-overall-download-limit" class="input-small" value="{{max-overall-download-limit}}" />
          </div>
        </div>
        <div class="control-group half">
          <label class="control-label" for="gsi-ul">$_LANG_Upload_Limit</label>
          <div class="controls">
            <input id="gsi-ul" name="max-overall-upload-limit" class="input-small" value="{{max-overall-upload-limit}}" />
          </div>
        </div>
        <div class="control-group half">
          <label class="control-label" for="gsi-cd">$_LANG_Concurrent_Downs</label>
          <div class="controls">
            <input id="gsi-cd" name="max-concurrent-downloads" class="input-small" value="{{max-concurrent-downloads}}" />
          </div>
        </div>
        <div class="control-group half">
          <label class="control-label" for="gsi-mss">$_LANG_Min_Split_Size</label>
          <div class="controls">
            <input id="gsi-mss" name="min-split-size" class="input-small" value="{{#_v.format_size_0}}{{min-split-size}}{{/_v.format_size_0}}" />
          </div>
        </div>
        <div class="clearfix"></div>

        <div class="control-group">
          <label class="control-label" for="gsi-ua">$_LANG_User_Agent</label>
          <div class="controls">
            <input id="gsi-ua" name="user-agent" class="input-xlarge" value="{{user-agent}}" />
          </div>
        </div>
        <div class="control-group">
          <label class="control-label" for="gsi-dir">$_LANG_Base_Dir</label>
          <div class="controls">
            <input id="gsi-dir" name="dir" class="input-xlarge" value="{{dir}}" disabled />
          </div>
        </div>
      </form>
    </script>

    <script src="js/jquery-1.7.2.min.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/jquery.jsonrpc.js"></script>
    <script src="js/jquery.Storage.js"></script>
    <script src="js/jquery.base64.min.js"></script>
    <script src="js/mustache.js"></script>
    <script src="js/peerid.js"></script>
    <script src="js/aria2.js"></script>
    <script src="js/yaaw.js"></script>
  </body>
</html>
<!-- vim: set et sw=2 ts=2 sts=2 ff=unix fenc=utf8: -->

EOF
