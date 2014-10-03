class FolderController < ApplicationController

  def create
    _check_auth()

    project = Project.find(params[:project_id])
    last_folder = project.get_last_folder_for_user(_user_id)

    data = {
      owner_id: _user_id,
      project_id: params[:project_id],
      name: 'New folder'
    }

    # block will be selected and commented
    folder = Folder.create!(data)
    if !folder.editable_by?(_user_id)
      _notify_admin()
      _no_access_show()

      return
    end

    # eveything to end of outer block will be selected and moved to new method
    users_ids = project.users.collect { |user| user.user_id }
    @user = User.find(_user_id)

    result = render(partial: 'workspace/folder', locals: {
      folder: folder,
      project: project
    })

    return result
  end

end